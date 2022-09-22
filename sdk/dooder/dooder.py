"""

"""

from typing import TYPE_CHECKING

from sdk.base.base_object import BaseObject
from sdk.dooder.cognition import Cognition
from sdk.dooder.fate import Fate
from sdk.dooder.genetics import Genetics
from sdk.dooder.util import get_direction
from sdk.environment.energy import Energy
from sdk.conditions.conditions import Conditions

if TYPE_CHECKING:
    from sdk.base.base_simulation import BaseSimulation


class Dooder(BaseObject):
    """ 

    """

    def __init__(self, unique_id: int, position: tuple, simulation: 'BaseSimulation') -> None:
        """
        Create a new Dooder object.

        Args:
            unique_id: Unique ID for the object.
            position: Starting position for the object.
            simulation: Reference to the simulation.
            params: Parameters for the simulation.

        Attributes:
            unique_id: Unique ID for the object.
            position: Starting position for the object.
            simulation: Reference to the simulation.
            params: Parameters for the simulation.
            energy: The energy level of the dooder.
            direction: The direction the dooder is facing.
            moore: The Moore neighborhood of the dooder.
            cognition: The cognition of the dooder.
            behavior: The behavior of the dooder.
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
        A dooder dies.

        Args:
            reason: The reason for the death.
        """
        self.simulation.society.terminate_dooder(self)
        message = f"Died from {reason}"

        self.log(granularity=1, message=message, scope='Dooder')
        
    def death_check(self) -> None:
        #! make this proccess a decorator or factory for easy creation of any conditional action
        """
        A dooder dies against condition checks
        """
        result, reason = Conditions.check_conditions('death', self)
        
        if result:
            self.die(reason)
            del self

            return True

        else:
            return False

    def choose_random_move(self) -> tuple:
        """
        Step one cell in any allowable direction.

        Returns:
            origin: The origin of the move.
            destination: The destination after the move.
        """
        #! have diff strategies for movement
        # Pick the next cell from the adjacent cells.
        possible_moves = self.simulation.environment.get_neighborhood(
            self.position, self.moore, True)

        origin = self.position
        destination = self.random.choice(possible_moves)

        return origin, destination

    def step(self) -> None:
        """
        Step the dooder.
        """
        #! Come up with a better design step flow.
        #! Have a simple way to easily change step flow
        
        #! need to double check doing this twice is a good idea
        if self.death_check():
            print("{} died in its sleep".format(self.unique_id))
            
        else:
            self.age += 1
            direction = 'None'
            cell_contents = self.simulation.environment.get_cell_list_contents(self.position)
            energy = [obj for obj in cell_contents if isinstance(obj, Energy)]
            neighbors = [obj for obj in cell_contents if isinstance(obj, Dooder)]
            
            if isinstance(energy, Energy):
                self.energy_supply += 1
                energy[0].consume()

            elif len(energy) == 1:
                self.energy_supply += 1
                e = energy[0]
                e.consume()
                self.log(
                    granularity=2, message=f"Consumed energy: {e.unique_id}", scope='Dooder')
                
            else:
                pass

            if Fate.ask_fate(self.MoveProbability):  # if true, move
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
    
    def __str__(self):
        """
        Return string of class attributes and genetics.
        """
        #! maybe come up with better formatting  
        return f"ID: {self.unique_id} \n Position: {self.position} \n Energy: {self.energy_supply} \n Age: {self.age} \n Genetics: {self.genetics}" 



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
