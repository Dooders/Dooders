""" 
Perception Module
-------------------
A perception is a list of Spaces adjacent to a Dooder.
"""

import random
from typing import TYPE_CHECKING, List, Tuple, Union

import numpy as np

if TYPE_CHECKING:
    from dooders.sdk.modules.space import Space


class Perception(list):
    """ 
    A perception is a list of Spaces that are adjacent to a dooder, 
    including the dooder's current Space

    Parameters
    ----------
    Space: list
        A list of Space adjacent to the dooder
    dooder: Dooder
        The dooder to create the perception around

    Attributes
    ----------
    __mapping__: dict
        A mapping of Space indices to directions

    Methods
    -------
    to_direction(Space: Location) -> str
        Convert the direction of a Space in the perception
    contains(object_type: str) -> list[bool]
        Check whether the perception contains a given object type
    fetch(object_type: str) -> list[object]
        Fetch all objects of a given type in the perception

    Properties
    ----------
    Spaces: list
        A list of Spaces adjacent to the dooder
    coordinates: list
        A list of coordinates of the Spaces in the perception
    random: Location
        A random Space in the perception
    """
    __mapping__ = {0: 'NW', 1: 'N', 2: 'NE', 3: 'W',
                   4: '-', 5: 'E', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self, spaces: list, dooder: object) -> None:
        self.dooder = dooder
        super().__init__(spaces)

    def to_direction(self, space: 'Space') -> str:
        """ 
        Convert the direction of a Space in the perception

        Parameters
        ----------
        Space: Location
            The Space to find the direction of
        """
        return self.__mapping__[space]

    def contains(self, object_type: str) -> List[bool]:
        """ 
        Check whether the perception contains a given object type

        Parameters
        ----------
        object_type: str
            The object type to check for

        Returns
        -------
        result: list[bool]
            True if the perception contains the object type, False otherwise
        """
        result = []
        for space in self:
            result.append(space.has(object_type, ignore=self.dooder))

        return result

    def fetch(self, object_type: str) -> List['object']:
        """ 
        Fetch a list of objects of a given type in the perception

        Parameters
        ----------
        object_type: str
            The object type to fetch

        Returns
        -------
        result: list[object]
            A list of objects of the given type
        """
        result = []
        for space in self:
            for contents in space.contents.values():
                if contents.__class__.__name__ == object_type:
                    result.append(contents)

        return result

    def array(self, objects: Union[str, List[str]]) -> List[int]:
        """ 
        Get the perception as an array of integers that represent the objects 
        in the perception. 1 = object is present, 0 = object is not present

        Parameters
        ----------
        objects: str or list[str]
            The object types to convert to

        Returns
        -------
        array: list[int]
            The perception as an array of objects

        Examples
        --------
        # With a list of objects
        >>> perception.array(['Dooder', 'Energy', 'Hazard'])
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        # With a single object
        >>> perception.array('Dooder')
        [1, 0, 0, 0, 0, 0, 0, 0, 0]
        """
        if isinstance(objects, str):
            objects = [objects]

        perception_array = []
        for object in objects:
            perception_array = perception_array + self.contains(object)

        return np.array([perception_array], dtype='uint8')

    @property
    def spaces(self) -> List['Space']:
        """ 
        Fetch a List of Spaces in the perception

        Returns
        -------
        Spaces: list[Location]
            The Spaces in the perception
        """
        return self

    @property
    def coordinates(self) -> List[Tuple[int, int]]:
        """ 
        Fetch the coordinates of the Spaces in the perception

        Returns
        -------
        coordinates: list[tuple[int, int]]
            The coordinates of the Spaces in the perception
        """
        return [x.coordinates for x in self]

    @property
    def random(self) -> 'Space':
        """ 
        Fetch random Space in the perception

        Returns
        -------
        Space: Location
            A random Space in the perception
        """
        return random.choice(self)
