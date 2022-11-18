""" 
This module contains the Neighborhood class, which is used to represent a
neighborhood in the simulation. A neighborhood is a list of locations.

#! make a neighborhood object that contains different data that usually comes bundled. Returns a list of location objects
#! attribute that returns a list of booleans. neighborhood.has('Energy') --> [0,1,0,0,0,1,1,0,0,0]
#! return only objects --> neighborhood.return('Energy') Energy, Dooder, Locations
"""

import random


class Neighborhood(list):
    """ 
    A neighborhood is a list of locations that are adjacent to a dooder, 
    including the dooder's current location
    """

    __mapping__ = {0: 'NW', 1: 'N', 2: 'NE', 3: 'W',
                   4: '-', 5: 'E', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self, locations, dooder):
        """ 
        Initialize a neighborhood object

        Args:
            dooder: The dooder to create the neighborhood around
        """
        self.dooder = dooder
        super().__init__(locations)

    def to_direction(self, location):
        """ 
        Return the direction of a location in the neighborhood

        Args:
            location: The location to find the direction of

        Returns:
            The direction of the location
        """
        return self.__mapping__[location]

    def contains(self, object_type: str):
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

    def fetch(self, object_type: str):
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
