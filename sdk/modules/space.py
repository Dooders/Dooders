""" 
Space Module
---------------

A Space object will correspond to a grid cell in the environment.
So, if the grid is 10x10, there will be 100 Spaces objects 
in the environment.

The Space class makes it easier to keep track of 
contents (Energy, Agents, etc.)
"""

import random


class Space:
    """ 
    Space object with a unique id and coordinates

    Parameters
    ----------
    x: int
        The x coordinate of the Space
    y: int
        The y coordinate of the Space

    Attributes
    ----------
    unique_id: str
        A unique id for the Space
    x: int
        See Parameters
    y: int
        See Parameters
    contents: dict
        A dictionary of objects in the Space
        The key is the unique id of the object,
        and the value is the object itself
    status: str
        The status of the Space (empty, occupied, etc.)

    Methods
    -------
    add(object: object) -> None
        Add an object to the Space
    remove(object: object) -> None
        Remove an object from the Space
    has(object_type: str, ignore=None) -> bool
        Return a boolean indicating if the Space contains
        a specific object type

    Properties
    ----------
    count: int
        Get the number of objects in the Space
    random: object
        Get a random object in the Space
    is_empty: bool
        Return a boolean indicating if the Space is empty
    is_occupied: bool
        Return a boolean indicating if the Space is occupied
    contents_pattern: str
        Return a string indicating the contents of the Space
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.contents: dict = {}
        self.status = 'empty'

    def add(self, object: object) -> None:
        """ 
        Add an object to the Space. 
        An object is added to the contents dictionary

        Parameters
        ----------
        object: object
            The object to add to the Space (i.e. Dooder, Energy, etc.)
        """
        self.contents[object.unique_id] = object
        self.status = 'occupied'

    def remove(self, object: object) -> None:
        """ 
        Remove an object from the Space

        Parameters
        ----------
        object: object
            The object to remove from the Space
        """
        self.contents.pop(object.unique_id, None)

        if len(self.contents) == 0:
            self.status = 'empty'

    def has(self, object_type: str, ignore=None) -> bool:
        """ 
        Return a boolean indicating if the Space contains 
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
            True if the Space contains the object type, False otherwise
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
        Get the number of objects in the Space

        Returns
        -------
        int
            The number of objects in the Space
        """
        return len(self.contents)

    @property
    def random(self) -> object:
        """ 
        Get a random object in the Space

        Returns
        -------
        object
            A random object in the Space
        """
        return random.choice(list(self.contents.values()))

    @property
    def is_empty(self) -> bool:
        """ 
        Return a boolean indicating if the Space is empty

        Returns
        -------
        bool
            True if the Space is empty, False otherwise
        """
        return self.status == 'empty'

    @property
    def is_occupied(self) -> bool:
        """ 
        Return a boolean indicating if the Space is occupied

        Returns
        -------
        bool
            True if the Space is occupied, False otherwise
        """
        return self.status == 'occupied'

    @property
    def contents_pattern(self) -> str:
        """ 
        Return a string of the contents of the Space

        The pattern is a list of integers representing each possible content state.

        The first integer is the number of contents in the Space that is a dooder object.
        The second integer is the number of contents in the Space that is an energy object.    

        So a total of 2 dooders and 1 energy would be 21.
        And, a total of 1 dooder and 2 energy would be 12.

        Returns
        -------
        pattern: str
            A string pattern of the contents of the Space
            See above for more details
        """
        first, second = 0, 0
        for content in self.contents.values():
            if content.name == 'Dooder':
                first += 1
            elif content.name == 'Energy':
                second += 1
        pattern = str(first) + str(second)

        return pattern
