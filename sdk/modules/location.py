""" 
Location
--------

A location object will correspond to a grid cell in the environment.
So, if the grid is 10x10, there will be 100 location objects 
in the environment.

The Location class makes it easier to keep track of 
contents (Energy, Agents, etc.)
"""

import random

#! need Location based attributes and collectors
#! every class can (and should) track information about itself
#! use tqdm to track progress
#! yep need a model abstract class like I have for policies, strategies, etc.
#! making attributes its own class to for tying attribute definition with collection
#! or is this just a collector???? dont need attributes class???
#! make collectors create and manage their own attributes???? what could go wrong


class Location:
    """ 
    Location object with a unique id and coordinates

    Parameters
    ----------
    x: int
        The x coordinate of the location
    y: int
        The y coordinate of the location

    Attributes
    ----------
    unique_id: str
        A unique id for the location
    x: int
        See Parameters
    y: int
        See Parameters
    contents: dict
        A dictionary of objects in the location
        The key is the unique id of the object,
        and the value is the object itself
    status: str
        The status of the location (empty, occupied, etc.)
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.contents: dict = {}
        self.status = 'empty'

    def add(self, object: object) -> None:
        """ 
        Add an object to the location. 
        An object is added to the contents dictionary

        Parameters
        ----------
        object: object
            The object to add to the location (i.e. Dooder, Energy, etc.)
        """
        self.contents[object.unique_id] = object
        self.status = 'occupied'

    def remove(self, object: object) -> None:
        """ 
        Remove an object from the location

        Parameters
        ----------
        object: object
            The object to remove from the location
        """
        self.contents.pop(object.unique_id, None)

        if len(self.contents) == 0:
            self.status = 'empty'

    def has(self, object_type: str, ignore=None) -> bool:
        """ 
        Return a boolean indicating if the location contains 
        a specific object type

        Parameters
        ----------
        object_type: str
            The type of object to check for
        ignore: object
            A list of object to ignore (Specifically the involved Dooder)

        Returns
        -------
        bool
            True if the location contains the object type, False otherwise
        """
        for object in self.contents.values():
            if object.__class__.__name__ == object_type:
                if ignore.unique_id == object.unique_id:
                    pass
                else:
                    return True
        return False
    
    def collect(self):
        # Create method to run through collection process for a location
        # should I have a model abstract class???
        # model collects its state and returns it
        pass

    @property
    def count(self) -> int:
        """ 
        Get the number of objects in the location

        Returns
        -------
        int
            The number of objects in the location
        """
        return len(self.contents)

    @property
    def random(self) -> object:
        """ 
        Get a random object in the location

        Returns
        -------
        object
            A random object in the location
        """
        return random.choice(list(self.contents.values()))

    @property
    def is_empty(self) -> bool:
        """ 
        Return a boolean indicating if the location is empty

        Returns
        -------
        bool
            True if the location is empty, False otherwise
        """
        return self.status == 'empty'

    @property
    def is_occupied(self) -> bool:
        """ 
        Return a boolean indicating if the location is occupied

        Returns
        -------
        bool
            True if the location is occupied, False otherwise
        """
        return self.status == 'occupied'
