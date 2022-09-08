from abc import ABC, abstractmethod
from typing import Type

ClassObject = Type[ABC]


class BaseTime(ABC):
    """ 

    """

    @abstractmethod
    def add(self, object: ClassObject) -> None:
        """
        Add an object to the schedule.

        Args:
            object: Object to add to the schedule
        """
        pass

    @abstractmethod
    def remove(self, object: ClassObject) -> None:
        """
        Remove all instances of a given agent from the schedule.

        Args:
            agent: An agent object.
        """
        pass

    @abstractmethod
    def _step(self, object_class: Type[ClassObject], shuffle_objects: bool = True) -> None:
        """ 
        Step through the objects of a given class

        Args:
            object_class: Class of objects to step through
            shuffle_objects: Whether to shuffle the objects before stepping through them
        """
        pass

    @abstractmethod
    def step(self, shuffle_types: bool = True, shuffle_objects: bool = True) -> None:
        """
        Execute the step of all the agents, one at a time.

        Args:
            shuffle_types: Whether to shuffle the types of objects before stepping through them
            shuffle_objects: Whether to shuffle the objects before stepping through them
        """
        pass
