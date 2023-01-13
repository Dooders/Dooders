""" 
Neighborhood
------------
Neighborhood class representS a neighborhood in the simulation. 
A neighborhood is a list of locations adjacent to a Dooder.
"""

import random
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from sdk.modules.location import Location


class Neighborhood(list):
    """ 
    A neighborhood is a list of locations that are adjacent to a dooder, 
    including the dooder's current location

    Parameters
    ----------
    locations: list
        A list of locations adjacent to the dooder
    dooder: Dooder
        The dooder to create the neighborhood around

    Attributes
    ----------
    __mapping__: dict
        A mapping of location indices to directions
    """

    __mapping__ = {0: 'NW', 1: 'N', 2: 'NE', 3: 'W',
                   4: '-', 5: 'E', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self, locations: list, dooder: object) -> None:
        self.dooder = dooder
        super().__init__(locations)

    def to_direction(self, location: 'Location') -> str:
        """ 
        Convert the direction of a location in the neighborhood

        Parameters
        ----------
        location: Location
            The location to find the direction of
        """
        return self.__mapping__[location]

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
        for location in self:
            result.append(location.has(object_type, ignore=self.dooder))

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
        for location in self:
            for contents in location.contents.values():
                if contents.__class__.__name__ == object_type:
                    result.append(contents)

        return result

    @property
    def locations(self) -> List['Location']:
        """ 
        Fetch a List of locations in the neighborhood

        Returns
        -------
        locations: list[Location]
            The locations in the neighborhood
        """
        return self

    @property
    def coordinates(self) -> List[Tuple[int, int]]:
        """ 
        Fetch the coordinates of the locations in the neighborhood

        Returns
        -------
        coordinates: list[tuple[int, int]]
            The coordinates of the locations in the neighborhood
        """
        return [x.coordinates for x in self]

    @property
    def random(self) -> 'Location':
        """ 
        Fetch random location in the neighborhood

        Returns
        -------
        location: Location
            A random location in the neighborhood
        """
        return random.choice(self)
