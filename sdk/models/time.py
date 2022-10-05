""" 

"""

import random
from collections import defaultdict
from typing import List, Type, Union

from sdk.base.base_object import BaseObject
from sdk.base.base_time import BaseTime, ClassObject

TimeT = Union[float, int]


class Time(BaseTime):
    """ 

    """

    def __init__(self) -> None:
        """
        Create a new, empty BaseScheduler.

        Attributes:
            steps: Number of steps taken in the simulation
            time: Current time in the simulation
            _objects: Dictionary of objects in the scheduler, 
                with agent class names as keys
        """
        # self.steps = 0
        self.random = random
        self.time: TimeT = 0  # ! What is the difference between time and steps?
        self._objects = defaultdict(dict)

    def add(self, object: 'BaseObject') -> None:
        """
        Add an object to the schedule.

        Args:
            object: Object to add to the schedule
        """

        if object.unique_id in self._objects[object.name]:
            raise Exception(
                f"Object with unique id {repr(object.unique_id)} already added to scheduler"
            )

        self._objects[object.name][object.unique_id] = object

    def remove(self, object: 'BaseObject') -> None:
        """
        Remove all instances of a given agent from the schedule.

        Args:
            object: An object being removed.
        """
        del self._objects[object.name][object.unique_id]

    def _step(self, object_class: Type[ClassObject], shuffle_objects: bool = True) -> None:
        """ 
        Step through the objects of a given class

        Args:
            object_class: Class of objects to step through
            shuffle_objects: Whether to shuffle the objects before stepping through them
        """
        object_keys = list(self._objects[object_class].keys())
        if shuffle_objects:
            self.random.shuffle(object_keys)
        for agent_key in object_keys:
            self._objects[object_class][agent_key].step()

    def step(self, shuffle_types: bool = True, shuffle_objects: bool = True) -> None:
        """
        Execute the step of all the agents, one at a time.

        Args:
            shuffle_types: Whether to shuffle the types of objects before stepping through them
            shuffle_objects: Whether to shuffle the objects before stepping through them
        """
        type_keys = list(self._objects.keys())
        if shuffle_types:
            self.random.shuffle(type_keys)
        for object_class in type_keys:
            self._step(object_class, shuffle_objects=shuffle_objects)
        # self.steps += 1
        self.time += 1

    def get_object_count(self, object_type: str) -> int:
        """
        Returns the current number of objects in the queue.

        Args:
            object_type: Class of objects to count

        Returns:
            The current number of objects in the queue.
        """
        return len(self._objects[object_type])

    def get_objects(self, object_class: ClassObject) -> List[ClassObject]:
        """ 
        Returns a list of all objects of a given class.

        Args:
            object_class: Class of objects to return

        Returns:
            A list of all objects of a given class.
        """
        return list(self._objects[object_class].values())

    def get_object(self, object_class: ClassObject, unique_id: int) -> ClassObject:
        """ 
        Returns an object of a given class with a given unique_id.

        Args:
            object_class: Class of object to return
            unique_id: Unique id of object to return

        Returns:
            An object of a given class with a given unique_id.
        """
        return self._objects[object_class][unique_id]
