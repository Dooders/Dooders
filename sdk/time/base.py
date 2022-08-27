from abc import ABC, abstractmethod
from typing import Type

ClassObject = Type[ABC]


class BaseTime(ABC):

    @abstractmethod
    def add(self, object: ClassObject) -> None:
        """Add an object to the schedule."""
        pass

    @abstractmethod
    def remove(self, object: ClassObject) -> None:
        """Remove all instances of a given agent from the schedule.
        Args:
            agent: An agent object.
        """
        pass

    @abstractmethod
    def _step(self, object_class: Type[ClassObject], shuffle_objects: bool = True) -> None:
        """ 
        """
        pass

    @abstractmethod
    def step(self, shuffle_types: bool = True, shuffle_objects: bool = True) -> None:
        """Execute the step of all the agents, one at a time."""
        pass
