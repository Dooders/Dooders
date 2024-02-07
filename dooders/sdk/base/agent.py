from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel

from dooders.sdk.base.coordinate import Coordinate
from dooders.sdk.models.information import Information

if TYPE_CHECKING:
    from dooders.sdk.base.simulation import Simulation


#! Need to define the best way to handle states


class BaseStats(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: str = None
    number: int = 0
    age: int = 0
    generation: int = 0
    birth: int = 0
    death: int = None
    position: Coordinate = Coordinate(0, 0)
    rotation: int = 0
    status: str = "Alive"
    reproduction_count: int = 0
    move_count: int = 0
    energy_consumed: int = 0
    hunger: int = 0
    tag: str = None
    encoded_weights: dict = {}
    inference_record: dict = {}


class Agent(ABC):
    """
    An agent is an entity that can move and interact with the environment

    Parameters
    ----------
    id : int
        Unique ID of the agent
    position : Coordinate
        Position of the agent, default (0, 0)
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
    update()
        Update the agent during a cycle

    Properties
    ----------
    name : str
        Name of the agent
    """

    def __init__(
        self, id: int, position: "Coordinate", simulation: "Simulation"
    ) -> None:
        self.cycle_number = simulation.cycle_number

        #! handle attributes better
        for attribute in BaseStats(
            id=id,
            position=position,
            rotation=0,
            generation=(self.cycle_number - 1) // 10 + 1,
            birth=self.cycle_number,
        ):
            setattr(self, attribute[0], attribute[1])

    def __del__(self) -> None:
        for attribute in BaseStats():
            setattr(self, attribute[0], None)

    def log(self, granularity: int, message: str, scope: str) -> None:
        """
        Log a message to the information object
        #! Might not need information class anymore, log directly

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
            "Scope": scope,
            "UniqueID": self.id,
            "CycleNumber": cycle_number,
            "Granularity": granularity,
            "Message": message,
        }

        final_message = str(log_dict).strip("{}")

        Information.log(final_message, granularity)

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError("Agent.update() not implemented")

    @property
    def name(self) -> str:
        """
        Returns
        -------
        str
            Name of the agent based on the class name
        """
        return self.__class__.__name__
