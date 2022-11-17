""" 
This module contains the Neighborhood class, which is used to represent a
neighborhood in the simulation. A neighborhood is a list of locations.

#! make a neighborhood object that contains different data that usually comes bundled. Returns a list of location objects
#! attribute that returns a list of booleans. neighborhood.has('Energy') --> [0,1,0,0,0,1,1,0,0,0]
#! return only objects --> neighborhood.return('Energy') Energy, Dooder, Locations
"""

import random

from sdk.models.dooder import Dooder
from sdk.models.energy import Energy


class Neighborhood(list):
    """ 
    A neighborhood is a list of locations that are adjacent to a dooder, 
    including the dooder's current location
    """

    __mapping__ = {0: 'N', 1: 'NE', 2: 'E', 3: 'SE',
                   4: 'S', 5: 'SW', 6: 'W', 7: 'NW', 8: '-'}

    def to_direction(self, location):
        """ 
        Return the direction of a location in the neighborhood

        Args:
            location: The location to find the direction of

        Returns:
            The direction of the location
        """
        return self.__mapping__[self.index(location)]

    def to_location(self, direction):
        """ 
        Return the location in a given direction

        Args:
            direction: The direction to find the location in

        Returns:
            The location in the given direction
        """
        return self[self.__mapping__.index(direction)]

    def contains(self, object_type):
        """ 
        Return whether the neighborhood contains a given object type

        Args:
            object_type: The object type to check for

        Returns:
            True if the neighborhood contains the object type, False otherwise
        """
        return [1 if isinstance(location, object_type) else 0 for location in self]

    @property
    def energy(self):
        """ 
        Return the energy in the neighborhood
        """
        return any([isinstance(x, Energy) for x in self])

    @property
    def dooder(self):
        """ 
        Return if dooder in the neighborhood
        """
        return any([isinstance(x, Dooder) for x in self])

    @property
    def locations(self):
        """ 
        Return the locations in the neighborhood
        """
        return self

    @property
    def coordinates(self):
        """ 
        Return the coordinates of the locations in the neighborhood
        """
        return [x.coordinates for x in self]

    @property
    def random(self):
        """ 
        Return a random location in the neighborhood
        """
        return random.choice(self)
