import random
from abc import ABC, abstractmethod

from pydantic import BaseModel

from dooders.sdk.models.information import Information


class BaseStats(BaseModel):
    id: str = None
    number: int = 0
    age: int = 0
    generation: int = 0
    birth: int = 0
    death: int = None
    position: tuple = None
    status: str = 'Alive'
    reproduction_count: int = 0
    move_count: int = 0
    energy_consumed: int = 0
    hunger: int = 0
    tag: str = None
    encoded_weights: dict = {}
    inference_record: dict = {}


class Agent(ABC):
    """ 
    Base Agent class

    Parameters
    ----------
    id : int
        Unique ID of the agent
    position : tuple
        Position of the agent
    simulation : Simulation
        Simulation object   

    Attributes
    ----------
    id : int
        Unique ID of the agent
    number : int
        Number of the agent
    age : int
        Age of the agent    
    generation : int
        Generation of the agent
    birth : int
        Birth cycle of the agent
    death : int
        Death cycle of the agent
    position : tuple
        Position of the agent
    status : str
        Status of the agent
    reproduction_count : int
        Number of times the agent has reproduced
    move_count : int
        Number of times the agent has moved
    energy_consumed : int
        Energy consumed by the agent
    hunger : int
        Hunger of the agent
    tag : str
        Tag of the agent
    encoded_weights : dict
        Encoded weights of the agent
    inference_record : dict
        Inference record of the agent

    Methods
    -------
    log(granularity: int, message: str, scope: str)
        Log a message to the information object
    step()
        Step function of the agent
    random
        Random object
    name
        Name of the agent
    """

    def __init__(self, id: int, position, simulation) -> None:
        self.simulation = simulation

        for attribute in BaseStats(id=id,
                                   position=position,
                                   generation=(
                                       simulation.cycle_number - 1) // 10 + 1,
                                   birth=simulation.cycle_number):
            setattr(self, attribute[0], attribute[1])

    def __del__(self) -> None:
        self.simulation = None
        for attribute in BaseStats():
            setattr(self, attribute[0], None)

    def log(self, granularity: int, message: str, scope: str) -> None:
        """ 
        Log a message to the information object

        Parameters
        ----------
        granularity : int
            Granularity of the message
        message : str
            Message to log
        scope : str
            Scope of the message
        """
        cycle_number = self.simulation.time.time

        log_dict = {
            'Scope': scope,
            'UniqueID': self.id,
            'CycleNumber': cycle_number,
            'Granularity': granularity,
            'Message': message
        }

        final_message = str(log_dict).strip('{}')

        Information.log(final_message, granularity)

    @abstractmethod
    def step(self) -> None:
        raise NotImplementedError('Agent.step() not implemented')

    @property
    def random(self) -> random.Random:
        """  
        Returns
        -------
        random.Random
            Random object
        """
        return self.simulation.random

    @property
    def name(self) -> str:
        """ 
        Returns
        -------
        str
            Name of the agent
        """
        return self.__class__.__name__
