""" 
Location class

A location object will correspond to a grid cell in the environment.
So, if the grid is 10x10, there will be 100 location objects in the environment.

The Location class makes it easier to keep track of contents (Energy, Agents, etc.)
"""

import random


class Location:

    def __init__(self, x: int, y: int) -> None:
        """ 
        Initialize a location object with a unique id and coordinates

        Args:
            x: The x coordinate of the location
            y: The y coordinate of the location

        Attributes:
            unique_id: A unique id for the location
            x: See Args
            y: See Args
            contents: A dictionary of objects in the location
                The key is the unique id of the object, and the value is the object itself
            status: The status of the location (empty, occupied, etc.)
        """
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.contents: dict = {}
        self.status = 'empty'

    def add(self, object: object) -> None:
        """ 
        Add an object to the location. 
        An object is added to the contents dictionary

        Args:
            object: The object to add to the location
        """
        self.contents[object.unique_id] = object
        self.status = 'occupied'

    def remove(self, object: object) -> None:
        """ 
        Remove an object from the location

        Args:
            object: The object to remove from the location
        """
        self.contents.pop(object.unique_id, None)

        if len(self.contents) == 0:
            self.status = 'empty'

    def has(self, object_type: str, ignore=None) -> bool:
        """ 
        Return a boolean indicating if the location contains a specific object type

        Args:
            object_type: The type of object to check for
            ignore: A list of object to ignore (Specifically the involved Dooder)
        """
        for object in self.contents.values():
            if object.__class__.__name__ == object_type:
                if ignore.unique_id == object.unique_id:
                    pass
                else:
                    return True
        return False

    @property
    def count(self) -> int:
        """ 
        Return the number of objects in the location
        """
        return len(self.contents)

    @property
    def random(self) -> object:
        """ 
        Return a random object in the location
        """
        return random.choice(list(self.contents.values()))

    @property
    def is_empty(self) -> bool:
        """ 
        Return a boolean indicating if the location is empty
        """
        return self.status == 'empty'

    @property
    def is_occupied(self) -> bool:
        """ 
        Return a boolean indicating if the location is occupied
        """
        return self.status == 'occupied'
