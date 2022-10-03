"""
A Dooder is a model object and the main focus of the library.
Each object will have the ability to move around the environment and
interact with other objects.
"""

from typing import TYPE_CHECKING

from sdk.base.base_object import BaseObject
from sdk.core import Condition
from sdk.core.data import Position, UniqueID
from sdk.modules.cognition import Cognition
from sdk.core.fate import Fate
from sdk.models.genetics import Genetics
from sdk.utils.get_direction import get_direction
from sdk.models.energy import Energy

if TYPE_CHECKING:
    from sdk.base.base_simulation import BaseSimulation


class Dooder(BaseObject):
    """ 
    Primary Dooder class
    """

    def __init__(self,
                 unique_id: 'UniqueID',
                 position: 'Position',
                 simulation: 'BaseSimulation') -> None:
        """
        Create a new Dooder object.

        Args:
            unique_id: Unique ID for the object. Created by the simulation object
            position: Starting position for the object. 
                The position ties to a location in the Environment object
            simulation: Reference to the simulation.

        Attributes:
            unique_id: see Args
            position: see Args
            simulation: see Args
            energy_supply: The energy level of the dooder.
            direction: The direction the dooder is facing.
            moore: The Moore neighborhood of the dooder.
            cognition: The cognition of the dooder.
            behavior: A mutable copy of a dooder's genetics. 
                Behavior serves as an expression of the genetics and the dodder's environment
            age: The number of cycles the dooder has been active.
        """
        super().__init__(unique_id, position, simulation)
        self.genetics = Genetics.compile_genetics(self)
        self.behavior = self.genetics.copy()
        self.cognition = Cognition()
        self.energy_supply = self.StartingEnergySupply
        self.direction = 'Origin'
        self.moore = True
        self.age = 0
        self.log(granularity=1,
                 message=f"Created", scope='Dooder')

    def kill(self, dooder: BaseObject) -> None:
        """ 
        Kill a dooder. 

        Args:
            dooder: The dooder to kill.
        """
        message = f"Killed by {self.unique_id}"
        dooder.die(message)

    def die(self, reason: str = 'Unknown') -> None:
        """
        Removing a dooder from the simulation, 
        with a given reason

        Args:
            reason: The reason for the death. 
                For example: starvation, old age, etc.
        """
        self.simulation.society.terminate_dooder(self)
        message = f"Died from {reason}"

        self.log(granularity=1, message=message, scope='Dooder')

    def death_check(self) -> None:
        """
        Checking if the dooder should be dead based on conditions of current state

        #TODO: make this process a decorator or factory for easy creation of any conditional action
        """
        result, reason = Condition.check_conditions('death', self)

        if result:
            self.die(reason)
            del self  # ! is this necessary?

            return True

        else:
            return False

    def choose_random_move(self) -> Position:
        """
        Step one cell in any allowable direction.

        Returns:
            origin: The origin of the move.
            destination: The destination after the move.

        #TODO: Movement based on a selected strategy
        """
        # Pick the next cell from the adjacent cells.
        possible_moves = self.simulation.environment.get_neighborhood(
            self.position, self.moore, True)

        origin = self.position
        destination = self.random.choice(possible_moves)

        return origin, destination

    def step(self) -> None:
        """
        Step flow for a dooder.

        Current flow:
        * Check if the dooder should die
        * Get cell contents
        * If there is energy in the current location, consume it
        * Check if the dooder should move and where
        * Move the dooder if success check is true
        * Check if the dooder should die based on step end state conditions

        #TODO Better step flow design
        #TODO Make it simple to change step flow

        """
        #! need to double check doing this twice is a good idea or necessary
        if self.death_check():
            print("{} died in its sleep".format(self.unique_id))

        else:
            self.age += 1
            direction = 'None'
            cell_contents = self.simulation.environment.get_cell_list_contents(
                self.position)
            energy = [obj for obj in cell_contents if isinstance(obj, Energy)]
            neighbors = [
                obj for obj in cell_contents if isinstance(obj, Dooder)]

            #! clean up this to log when first if statement is true
            if isinstance(energy, Energy):
                self.energy_supply += 1
                energy[0].consume()

            elif len(energy) == 1:
                self.energy_supply += 1
                e = energy[0]
                e.consume()
                self.log(
                    granularity=2, message=f"Consumed energy: {e.unique_id}", scope='Dooder')

            else:  # No energy to consume
                pass

            if Fate.ask_fate(self.MoveProbability):  # if true, decide where to move
                origin, destination = self.choose_random_move()

                if origin != None:
                    new_direction = get_direction(origin, destination)
                else:
                    new_direction = get_direction(self.position, destination)

                # if true, successfully move
                if Fate.ask_fate(self.MoveSuccessProbability):
                    self.simulation.environment.move_object(self, destination)
                    self.energy_supply -= 1
                    direction = new_direction
                    self.position = destination
                    self.log(
                        granularity=2, message=f"Moved {direction} from {origin} to {destination}", scope='Dooder')
                else:
                    self.energy_supply -= 1
                    self.log(
                        granularity=3, message=f"Failed to move {direction} from {origin} to {destination}", scope='Dooder')
            else:
                direction = 'None'
                self.log(
                    granularity=3, message=f"Skipped move", scope='Dooder')

            self.direction = direction

            if self.death_check():
                print('{} died during its cycle'.format(self.unique_id))

    def __str__(self) -> str:
        """
        Return string of class attributes and genetics.
        """
        #! maybe come up with better formatting
        return f"ID: {self.unique_id} \n Position: {self.position} \n Energy: {self.energy_supply} \n Age: {self.age} \n Genetics: {self.genetics}"

    @property
    def stats(self) -> dict:
        """
        Return a dictionary of the dooder's stats.
        """
        stats = {
            'cycle_number': self.simulation.time.time,
            'unique_id': self.unique_id,
            'position': self.position,
            'energy_supply': self.energy_supply,
            'direction': self.direction,
            'age': self.age
        }

        return stats

# Todo: Create an Effects class (can be temporary or permanent)

#! Every end of cycle there will be a check to check fate if the dooder will die
#! The probability of death will go either up or down depending on multiple factors and effects
#! So survivability is a function of the effects of genetics, environment, and behavior
#! Then I can train an agent to maximize days alive and survivability
#! Maybe even have the ability to change how fate is determined


##### Formulas #####

# #! Survivability modifier
# Every dooder starts with 99.99% probability surviving the cycle
# The modifier will reduce the probability of survival to be checked at the end of each cycle
# survival_probability_modifier = (negative_effects + positive_effects) + permanent_effects

# #! Hunger (temporary negative effect)
# Calculates the hunger slevel of the dooder
# Added to negative_effects
# M = Metabolism (between 1 and 2)
# hunger = M^(number of cycle hungry) more cycle will add more negative probability

# #! Age (permanent negative effect)
# As a dooder goes through more cycles, it will have a higher chance of dying
# Needs to have a long time as low probability to die then at some point it will increase by a lot
# Age deterioration can be a genetic thing too

# !# Mood (temporary positive or negative effect)
# Based on a lot of different factors
# Between -100 and 100 or -1 and 1
# """
