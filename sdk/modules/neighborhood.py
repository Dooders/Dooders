""" 
Neighborhood Class

This module contains the Neighborhood class, which is used to represent a
neighborhood in the simulation. A neighborhood is a list of locations adjacent to a Dooder.
"""

import random
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from sdk.modules.location import Location


class Neighborhood(list):
    """ 
    A neighborhood is a list of locations that are adjacent to a dooder, 
    including the dooder's current location
    """

    __mapping__ = {0: 'NW', 1: 'N', 2: 'NE', 3: 'W',
                   4: '-', 5: 'E', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self, locations, dooder: object) -> None:
        """ 
        Initialize a neighborhood object

        Args:
            locations: A list of locations adjacent to the dooder
            dooder: The dooder to create the neighborhood around
        """
        self.dooder = dooder
        super().__init__(locations)

    def to_direction(self, location: 'Location') -> str:
        """ 
        Return the direction of a location in the neighborhood

        Args:
            location: The location to find the direction of

        Returns:
            The direction of the location
        """
        return self.__mapping__[location]

    def contains(self, object_type: str) -> bool:
        """ 
        Return whether the neighborhood contains a given object type

        Args:
            object_type: The object type to check for

        Returns:
            True if the neighborhood contains the object type, False otherwise
        """
        result = []
        for location in self:
            result.append(location.has(object_type, ignore=self.dooder))

        return result

    def fetch(self, object_type: str) -> object:
        """ 
        Return a list of objects of a given type in the neighborhood

        Args:
            object_type: The object type to fetch

        Returns:
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
        Return the locations in the neighborhood
        """
        return self

    @property
    def coordinates(self) -> List[Tuple[int, int]]:
        """ 
        Return the coordinates of the locations in the neighborhood
        """
        return [x.coordinates for x in self]

    @property
    def random(self) -> 'Location':
        """ 
        Return a random location in the neighborhood
        """
        return random.choice(self)
