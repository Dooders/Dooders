"""
Dooder
------
A Dooder is a model object and the main focus of the library.
Each object will have the ability to move around the environment and
interact with other objects.
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel

from dooders.sdk import steps
from dooders.sdk.base.base_agent import BaseAgent
from dooders.sdk.core import Condition
from dooders.sdk.core.action import Action
from dooders.sdk.core.step import Step
from dooders.sdk.modules.cognition import Cognition
from dooders.sdk.modules.internal_models import InternalModels
from dooders.sdk.modules.neighborhood import Neighborhood

if TYPE_CHECKING:
    from dooders.sdk.base.reality import BaseSimulation


MotivationList = ['Consume', 'Reproduce']


class MainStats(BaseModel):
    id: str
    position: tuple
    hunger: int
    age: int
    birth: int
    status: str
    reproduction_count: int
    move_count: int
    energy_consumed: int


class Dooder(BaseAgent):
    """ 
    Primary Dooder class

    Parameters
    ----------
    id: str
        Unique ID for the object. 
        Created by the simulation object
    position: tuple
        Position of the object.
        The position ties to a location in the Environment object
    simulation: BaseSimulation
        Reference to the simulation.

    Attributes
    ----------
    genetics: Genetics
        The genetics of the dooder. WIP
    behavior: dict
        A mutable copy of a dooder's genetics.
        Behavior serves as an expression of the genetics and the dodder's environment
    cognition: Cognition
        The cognition of the dooder. WIP
    direction: str
        The direction the dooder recently moved.
    moore: bool
        The Moore neighborhood of the dooder.
    internal_models: InternalModels
        The internal models of the dooder.

    Methods
    -------
    do(action: str)
        Dooder action flow
    die(reason: str = 'Unknown')
        Removing a dooder from the simulation, with a given reason
    death_check()
        Checking if the dooder should be dead, based on conditions of current state
    step()
        Step flow for a dooder.
    find_partner()
        Find another Dooder from current position.

    Properties
    ----------
    main_stats: MainStats
        The main stats of the dooder.
    neighborhood: Neighborhood
        The neighborhood of the dooder.
    """

    def __init__(self,
                 id: 'UniqueID',
                 position: 'Position',
                 simulation: 'BaseSimulation') -> None:

        super().__init__(id, position, simulation)
        # self.genetics = Genetics.compile_genetics(self)
        # self.behavior = self.genetics.copy()
        self.cognition = Cognition()
        self.direction = 'Origin'
        self.moore = True
        self.internal_models = InternalModels(MotivationList)
        self.log(granularity=1,
                 message=f"Created",
                 scope='Dooder')

    def do(self, action: str) -> None:
        """ 
        Dooder action flow

        Parameters
        ----------
        action: str
            The action to be taken
        """
        Action.execute(self, action)

    def die(self, reason: str = 'Unknown') -> None:
        """
        Removing a dooder from the simulation, 
        with a given reason

        Parameters
        ----------
        reason: str
            The reason for the death. 
            For example: starvation, old age, etc.
        """
        self.simulation.arena.terminate_dooder(self)
        message = f"Died from {reason}"

        self.log(granularity=1, message=message, scope='Dooder')

    def death_check(self) -> None:
        """
        Checking if the dooder should be dead,
        based on conditions of current state
        """
        result, reason = Condition.check('death', self)

        if result:
            self.die(reason)

            return True

        else:
            return False

    def step(self) -> None:
        """
        Step flow for a dooder.

        Process
        -------
        1. Increment age
        2. Check if the dooder should die at the beginning of its step
        3. Perform the step from the Step class
        4. Check if the dooder should die at the end of its step

        """
        self.age += 1

        if self.death_check():
            self.log(granularity=1,
                     message="Terminated between cycles",
                     scope='Dooder')
        else:
            Step.forward('BasicStep', self)

            if self.death_check():
                self.log(granularity=1,
                         message="Terminated during cycle",
                         scope='Dooder')

    def find_partner(self) -> 'Dooder':
        #! Make this an action and model? Yes
        """
        Find another Dooder from current position.

        Returns
        -------
        partner: Dooder
            A Dooder object, if found.
        """
        near_dooders = self.simulation.environment.contents(
            self.position)

        for object in near_dooders:
            if isinstance(object, Dooder) and object.id != self.id:
                return object

        return None

    # def __str__(self) -> str:
    #     """
    #     Return string of class attributes and genetics.

    #     Returns
    #     -------
    #     string: str
    #         A string of the dooder's attributes and genetics.
    #     """
    #     return f"UniqueID: {self.id} \n Position: {self.position} \n Hunger: {self.hunger} \n Age: {self.age} \n Genetics: {self.genetics}"

    @property
    def history(self) -> list:
        """ 
        Return the dooder's history.

        Returns
        -------
        logs: list
            A list of dictionaries of the dooder's history.
        """
        logs = []
        for log in self.simulation.load_log():
            if log.get('UniqueID') == self.id:
                logs.append(log)
        return logs

    @property
    def stats(self) -> 'MainStats':
        """
        The base stats of the dooder.

        Returns
        -------
        stats: dict 
            A dictionary of the dooder's main stats.
            for example: 
            {'id': '1234', 'position': (0,0), 'hunger': 0, 
            'age': 4, 'birth': 0, 'status': 'Alive', 'reproduction_count': 0, 
            'move_count': 0, 'energy_consumed': 0}
        """
        stats = {}
        for stat in MainStats.__fields__:
            stats[stat] = getattr(self, stat)

        return MainStats(**stats)

    @property
    def neighborhood(self) -> 'Neighborhood':
        """
        Return a list of the dooder's neighborhood locations.

        Returns
        -------
        neighborhood: list
            A list of the dooder's nearby neighborhood locations.
        """
        locations = self.simulation.environment.nearby_spaces((self.position))

        return Neighborhood(locations, self)
    
    @property
    def state(self):
        return self.stats.dict()
