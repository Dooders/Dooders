""" 
Neighborhood Module
-------------------
Neighborhood class representS a neighborhood in the simulation. 
A neighborhood is a list of Spaces adjacent to a Dooder.
"""

import random
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from sdk.modules.space import Space


class Neighborhood(list):
    """ 
    A neighborhood is a list of Spaces that are adjacent to a dooder, 
    including the dooder's current Space

    Parameters
    ----------
    Space: list
        A list of Space adjacent to the dooder
    dooder: Dooder
        The dooder to create the neighborhood around

    Attributes
    ----------
    __mapping__: dict
        A mapping of Space indices to directions
        
    Methods
    -------
    to_direction(Space: Location) -> str
        Convert the direction of a Space in the neighborhood
    contains(object_type: str) -> list[bool]
        Check whether the neighborhood contains a given object type
    fetch(object_type: str) -> list[object]
        Fetch all objects of a given type in the neighborhood
        
    Properties
    ----------
    Spaces: list
        A list of Spaces adjacent to the dooder
    coordinates: list
        A list of coordinates of the Spaces in the neighborhood
    random: Location
        A random Space in the neighborhood
    """

    __mapping__ = {0: 'NW', 1: 'N', 2: 'NE', 3: 'W',
                   4: '-', 5: 'E', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self, spaces: list, dooder: object) -> None:
        self.dooder = dooder
        super().__init__(spaces)

    def to_direction(self, space: 'Space') -> str:
        """ 
        Convert the direction of a Space in the neighborhood

        Parameters
        ----------
        Space: Location
            The Space to find the direction of
        """
        return self.__mapping__[space]

    def contains(self, object_type: str) -> List[bool]:
        """ 
        Check whether the neighborhood contains a given object type

        Parameters
        ----------
        object_type: str
            The object type to check for

        Returns
        -------
        result: list[bool]
            True if the neighborhood contains the object type, False otherwise
        """
        result = []
        for space in self:
            result.append(space.has(object_type, ignore=self.dooder))

        return result

    def fetch(self, object_type: str) -> List['object']:
        """ 
        Fetch a list of objects of a given type in the neighborhood

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

    @property
    def spaces(self) -> List['Space']:
        """ 
        Fetch a List of Spaces in the neighborhood

        Returns
        -------
        Spaces: list[Location]
            The Spaces in the neighborhood
        """
        return self

    @property
    def coordinates(self) -> List[Tuple[int, int]]:
        """ 
        Fetch the coordinates of the Spaces in the neighborhood

        Returns
        -------
        coordinates: list[tuple[int, int]]
            The coordinates of the Spaces in the neighborhood
        """
        return [x.coordinates for x in self]

    @property
    def random(self) -> 'Space':
        """ 
        Fetch random Space in the neighborhood

        Returns
        -------
        Space: Location
            A random Space in the neighborhood
        """
        return random.choice(self)
