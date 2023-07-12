"""
Dooder
------
A Dooder is a model object and the main focus of the library.
Each object will have the ability to move around the environment and
interact with other objects.
"""

from typing import TYPE_CHECKING, Any, List

import numpy as np
from pydantic import BaseModel

from dooders.sdk import steps
from dooders.sdk.base.agent import Agent
from dooders.sdk.core import Condition
from dooders.sdk.core.action import Action
from dooders.sdk.core.step import Step
from dooders.sdk.modules.internal_models import InternalModels
from dooders.sdk.modules.perception import Perception

if TYPE_CHECKING:
    from dooders.sdk.base.reality import BaseSimulation


MotivationList = ['Consume', 'Reproduce']


class MainStats(BaseModel):
    id: str
    number: int
    position: tuple
    hunger: int
    age: int
    generation: int
    birth: int
    death: int = None
    status: str
    reproduction_count: int
    move_count: int
    energy_consumed: int
    tag: str
    encoded_weights: dict
    inference_record: dict


class Dooder(Agent):
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
    perception: Perception
        The Dooder's perception.
    """

    def __init__(self, id: str, position: tuple, simulation: 'BaseSimulation') -> None:
        super().__init__(id, position, simulation)
        self.moore = True
        self.condensed_weight_list = list()
        self.internal_models = InternalModels(MotivationList, self.id)
        self.log(granularity=1, message=f"Created", scope='Dooder')

    def __del__(self):
        self.condensed_weight_list = list()
        self.internal_models = None
        self.simulation = None

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
        self.status = 'Terminated'
        self.death = self.simulation.cycle_number
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
        self.get_gene_embedding()
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

    def get_gene_embedding(self) -> None:
        """ 
        Post step flow for a dooder.

        Process
        -------
        1. Update encoded weights
        2. Update condensed weights
        """
        encoded_weights_value = list(self.get_encoded_weights)
        cycle_number = self.simulation.cycle_number
        self.encoded_weights[cycle_number] = encoded_weights_value

    def find_partner(self) -> 'Dooder':
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

    @property
    def get_encoded_weights(self) -> np.ndarray:
        """ 
        Get the encoded weights of the dooder.

        Returns
        -------
        encoded_weights: np.ndarray
            The encoded weights of the dooder.
        """
        # PCA transform of internal model weights
        # {model_name: condensed_weight_tuple} i.e. {'Consume': (1, 132, 103)}
        weights = self.weights['Consume'][1]
        embedding = self.gene_embedding.fit(weights)
        return embedding.singular_values_

    @property
    def weights(self) -> dict:
        """ 
        Get the weights of the dooder.

        Returns
        -------
        weights: dict
            The weights of the dooder.
        """
        return self.internal_models.weights

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
    def perception(self) -> 'Perception':
        """
        Return a list of the dooder's perception locations.

        Returns
        -------
        perception: list
            A list of the dooder's nearby perception locations.
        """
        locations = self.simulation.environment.nearby_spaces((self.position))

        return Perception(locations, self)

    @property
    def state(self) -> dict:
        """ 
        Return the state of the dooder.

        Returns
        -------
        state: dict
            The state of the dooder.
        """
        state = self.stats.dict()
        state['encoded_weights'] = self.encoded_weights
        return state

    @property
    def final_state(self):
        """ 
        Return the final state of the dooder.

        Returns
        -------
        state: dict
            The final state of the dooder.
        """
        state = self.state
        state['final_state'] = self.weights['Consume'][0]
        return state
