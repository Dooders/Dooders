"""
A Dooder is a model object and the main focus of the library.
Each object will have the ability to move around the environment and
interact with other objects.
"""

import copy
from typing import TYPE_CHECKING

from sdk.actions.reproduce import reproduce
from sdk.base.base_object import BaseObject
from sdk.core import Condition
from sdk.models.energy import Energy
from sdk.models.genetics import Genetics
from sdk.modules.cognition import Cognition
from sdk.modules.internal_models import InternalModels
from sdk.modules.neighborhood import Neighborhood
from sdk.utils.get_direction import get_direction

if TYPE_CHECKING:
    from sdk.base.base_simulation import BaseSimulation

    
MotivationList = ['Consume', 'Reproduce']
    

class Dooder(BaseObject):
    """ 
    Primary Dooder class
    """

    def __init__(self,
                 unique_id,
                 position,
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
            hunger: Hunger level of the dooder.
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
        self.hunger = 0
        self.direction = 'Origin'
        self.moore = True
        self.age = 0
        self.internal_models = InternalModels(MotivationList)
        self.log(granularity=1,
                 message=f"Created", scope='Dooder')

    def move(self, destination):
        if destination == self.position:
            pass
        else:
            origin = self.position
            self.direction = get_direction(origin, destination)
            self.simulation.environment.move_object(self, destination)
            self.log(
                granularity=2, message=f"Moved {self.direction} from {origin} to {destination}", scope='Dooder')
            self.position = destination

    def consume(self):
        """ 
        Consume energy from the environment
        """

        cell_contents = self.simulation.environment.get_cell_list_contents(
            self.position)
        energy = [obj for obj in cell_contents if isinstance(obj, Energy)]

        if energy:
            food = energy[0]
            food.consume()
            if self.hunger > 0:
                self.hunger = 0
            # elif self.hunger <= 0:
            #     self.hunger += -1
            self.log(
                granularity=2, message=f"Consumed energy: {food.unique_id}", scope='Dooder')
        else:
            self.hunger += 1

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
        """
        result, reason = Condition.check_conditions('death', self)

        if result:
            self.die(reason)
            del self  # ! is this necessary?

            return True

        else:
            return False

    def step(self) -> None:
        """
        Step flow for a dooder.

        Current flow:
        * TBD
        """

        self.age += 1

        if self.death_check():
            self.log(granularity=1,
                     message="Terminated between cycles", scope='Dooder')

        else:
            policy = self.simulation.params.get('Policies').Movement
            destination = self.simulation.policies(policy, self)
            self.move(destination)
            self.consume()
            reproduce(self)

            if self.death_check():
                self.log(granularity=1,
                         message="Terminated during cycle", scope='Dooder')

    def clone(self):
        """
        Clone the dooder.
        """
        clone = copy.deepcopy(self)
        clone.unique_id = self.simulation.seed.uuid()

        return clone
    
    def find_partner(self) -> 'Dooder':
        """
        Find another Dooder from current position.
        """
        near_dooders = self.simulation.environment.get_cell_list_contents(self.position)

        for object in near_dooders:
            if isinstance(object, Dooder):
                return object

        return None
        
    def __str__(self) -> str:
        """
        Return string of class attributes and genetics.
        """
        #! maybe come up with better formatting
        return f"UniqueID: {self.unique_id} \n Position: {self.position} \n Hunger: {self.hunger} \n Age: {self.age} \n Genetics: {self.genetics}"

    @property
    def stats(self) -> dict:
        """
        Return a dictionary of the dooder's stats.
        """
        stats = {
            'CycleNumber': self.simulation.time.time,
            'UniqueID': self.unique_id,
            'Position': self.position,
            'Hunger': self.hunger,
            'Direction': self.direction,
            'Age': self.age
        }

        return stats

    @property
    def neighborhood(self) -> list:
        """
        Return a list of the dooder's neighborhood locations.
        """
        locations = self.simulation.environment.get_neighbor_locations(
            (self.position))

        return Neighborhood(locations, self)


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
