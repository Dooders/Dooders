""" 
Location class
"""

import random


class Location:

    # List of all contents in the location
    def __init__(self, x, y):
        """ 
        Initialize a location object with a unique id and coordinates

        Args:
            x: The x coordinate of the location
            y: The y coordinate of the location

        Returns:
            A location object
        """
        self.contents: dict = {}
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.status = 'empty'

    def add(self, object):
        """ 
        Add an object to the location

        Args:
            object: The object to add to the location
        """
        self.contents[object.unique_id] = object
        self.status = 'occupied'

    def remove(self, object):
        """ 
        Remove an object from the location

        Args:
            object: The object to remove from the location
        """
        self.contents.pop(object.unique_id, None)

        if len(self.contents) == 0:
            self.status = 'empty'

    @property
    def count(self):
        """ 
        Return the number of objects in the location
        """
        return len(self.contents)

    @property
    def random(self):
        """ 
        Return a random object in the location
        """
        return random.choice(list(self.contents.values()))

    def has(self, object_type, ignore=None):
        """ 
        Return a boolean indicating if the location contains a specific object type
        """
        for object in self.contents.values():
            if object.__class__.__name__ == object_type:
                if ignore.unique_id == object.unique_id:
                    pass
                else:
                    return True
        return False
