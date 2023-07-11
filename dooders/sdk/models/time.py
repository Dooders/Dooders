""" 
Time Model
----------
Responsible for managing the time of the simulation. 
Essentially, the order in which agents are stepped through during a cycle.
"""

import random
from collections import defaultdict

from dooders.sdk.base.agent import Agent
from dooders.sdk.base.base_time import BaseTime


class Time(BaseTime):
    """ 
    Class manages the passage of time in the simulation. 

    Each cycle all Dooder objects are stepped through.

    Attributes
    ----------
    time : int
        The current time in the simulation (number of cycles).
    _objects : dict
        Dictionary of objects in the scheduler, with agent class names as keys.
    random : Random
        The random number generator used by the scheduler.

    Methods
    -------
    add(object)
        Add an object to the schedule.
    remove(object)
        Remove all instances of a given agent from the schedule.
    step()
        Step through the schedule.
    _step(object_class, shuffle)
        Step through the schedule for a given object class.
    """

    __slots__ = ["time", "_objects", "random"]

    def __init__(self) -> None:
        self.random = random
        self.time = 0
        self._objects = defaultdict(dict)

    def add(self, object: 'Agent') -> None:
        """
        Add an object to the schedule.

        Parameters
        ----------
        object: Object
            add to the schedule
        """

        if object.id in self._objects[object.name]:
            raise Exception(
                f"Object with unique id {repr(object.id)} already added to scheduler"
            )

        self._objects[object.name][object.id] = object

    def remove(self, object: 'Agent') -> None:
        """
        Remove all instances of a given agent from the schedule.

        Parameters
        ----------
        object: Object
            Object being removed.
        """
        del self._objects[object.name][object.id]

    def _step(self, object_class: str, shuffle_objects: bool = True) -> None:
        """ 
        Step through the objects of a given class

        Parameters
        ----------
        object_class: str
            Class of objects to step through
        shuffle_objects: bool
            Whether to shuffle the objects before stepping through them
        """
        object_keys = list(self._objects[object_class].keys())
        if shuffle_objects:
            self.random.shuffle(object_keys)
        for agent_key in object_keys:
            self._objects[object_class][agent_key].step()

    def step(self, shuffle_types: bool = True, shuffle_objects: bool = True) -> None:
        """
        Execute the step of all the agents, one at a time.

        Parameters
        ----------
        shuffle_types: bool
            Whether to shuffle the types of objects before stepping through them
        shuffle_objects: bool
            Whether to shuffle the objects before stepping through them
        """
        type_keys = list(self._objects.keys())
        if shuffle_types:
            self.random.shuffle(type_keys)
        for object_class in type_keys:
            self._step(object_class, shuffle_objects=shuffle_objects)

        self.time += 1

    def get_object_count(self, object_type: str) -> int:
        """
        Returns the current number of objects in the queue,
        based on the object type.

        Parameters
        ----------
        object_type: str 
            Class of objects to count

        Returns
        -------
        count: int    
            The current number of objects in the queue.
        """
        return len(self._objects[object_type])

    def get_objects(self, object_class: str) -> list:
        """ 
        Returns a list of all objects of a given class.

        Parameters
        ----------
        object_class: str
            Class of objects to return

        Returns
        -------
        objects: list
            All objects of a given class.
        """
        return list(self._objects[object_class].values())

    def get_object(self, object_class: str, id: int) -> 'Agent':
        """ 
        Returns an object of a given class with a given id.

        Parameters
        ----------
        object_class: str
            Class of object to return
        id: str
            Unique id of object to return

        Returns
        -------
        object: Object 
            An object of a given class with a given id.
        """
        return self._objects[object_class][id]
