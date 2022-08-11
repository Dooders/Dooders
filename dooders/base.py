from abc import ABC, abstractmethod
from random import Random

from dooders.behavior import Behavior
from dooders.cognition import Cognition


class BaseDooder(ABC):
    """
    Base class for all dooders.
    """

    def __init__(self, unique_id: int, position, model) -> None:
        """
        Create a new dooder agent.

        Args:
            unique_id: A unique numeric identified for the agent
            model: Instance of the simulation object that contains the agent
            position: The (x, y) position of the agent
        """
        self.unique_id = unique_id
        self.model = model
        self.position: position
        self.behavior = Behavior()
        self.cognition = Cognition()
        self.environment = model.environment
        self.information = model.information

    def log(self, granularity: int, message: str) -> None:
        # get specific dooder instance details and send to information object
        cycle_number = self.model.schedule.time
        final_message = f"{self.unique_id} - {cycle_number} - {granularity} - {message}"

        self.information.log(final_message, granularity)

    @abstractmethod
    def step(self) -> None:
        pass

    @property
    def random(self) -> Random:
        return self.model.random


class BaseInformation():
    def __init__(self) -> None:
        pass

    def collect():
        pass
