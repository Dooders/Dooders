import random
from collections import defaultdict
from typing import List, Type, Union

from sdk.time.base import BaseTime, ClassObject

TimeT = Union[float, int]

class Time(BaseTime):

    def __init__(self) -> None:
        """Create a new, empty BaseScheduler."""
        self.steps = 0
        self.random = random
        self.time: TimeT = 0  # ! What is the difference between time and steps?
        self._objects = defaultdict(dict)

    def add(self, object) -> None:
        """
        """

        if object.unique_id in self._objects[object.name]:
            raise Exception(
                f"Object with unique id {repr(object.unique_id)} already added to scheduler"
            )

        self._objects[object.name][object.unique_id] = object

    def remove(self, object) -> None:
        """Remove all instances of a given agent from the schedule.
        Args:
            agent: An agent object.
        """
        del self._objects[object.name][object.unique_id]

    def _step(self, object_class: Type[ClassObject], shuffle_objects: bool = True) -> None:
        """ 
        """
        object_keys = list(self._objects[object_class].keys())
        if shuffle_objects:
            self.random.shuffle(object_keys)
        for agent_key in object_keys:
            self._objects[object_class][agent_key].step()

    def step(self, shuffle_types: bool = True, shuffle_objects: bool = True) -> None:
        """Execute the step of all the agents, one at a time."""
        type_keys = list(self._objects.keys())
        if shuffle_types:
            self.random.shuffle(type_keys)
        for object_class in type_keys:
            self._step(object_class, shuffle_objects=shuffle_objects)
        self.steps += 1
        self.time += 1

    def get_object_count(self, object_type) -> int:
        """Returns the current number of agents in the queue."""
        return len(self._objects[object_type])

    def get_objects(self, object_class: ClassObject) -> List[ClassObject]:
        return list(self._objects[object_class].values())

    def get_object(self, object_class: ClassObject, unique_id: int) -> ClassObject:
        return self._objects[object_class][unique_id]
    