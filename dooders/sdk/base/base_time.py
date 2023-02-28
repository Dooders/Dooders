from abc import ABC, abstractmethod


class BaseTime(ABC):
    """ 
    Base class for the Time model.
    Having this class makes it simpler to experiment with different time logic
    """

    @abstractmethod
    def add(self, object: object) -> None:
        """
        Add an object to the schedule.

        Args:
            object: Object to add to the schedule
        """
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def remove(self, object: object) -> None:
        """
        Remove all instances of a given agent from the schedule.

        Args:
            agent: An agent object.
        """
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def _step(self, object_class: object, shuffle_objects: bool = True) -> None:
        """ 
        Step through the objects of a given class

        Args:
            object_class: Class of objects to step through
            shuffle_objects: Whether to shuffle the objects before stepping through them
        """
        raise NotImplementedError("Subclass must implement this method")

    @abstractmethod
    def step(self, shuffle_types: bool = True, shuffle_objects: bool = True) -> None:
        """
        Execute the step of all the agents, one at a time.

        Args:
            shuffle_types: Whether to shuffle the types of objects before stepping through them
            shuffle_objects: Whether to shuffle the objects before stepping through them
        """
        raise NotImplementedError("Subclass must implement this method")
