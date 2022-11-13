# slicing
# turn list of locations to: list of location coordinates, list of energy/dooder objects, return if conditionals

import random

from sdk.models import Energy, Dooder


class Neighborhood(list):

    __mapping__ = {0: 'N', 1: 'NE', 2: 'E', 3: 'SE',
                   4: 'S', 5: 'SW', 6: 'W', 7: 'NW', 8: '-'}

    def to_direction(self, location):
        return self.__mapping__[self.index(location)]

    def to_location(self, direction):
        return self[self.__mapping__.index(direction)]

    def contains(self, object_type):
        return [1 if isinstance(location, object_type) else 0 for location in self]

    @property
    def energy(self):
        return any([isinstance(x, Energy) for x in self])

    @property
    def dooder(self):
        return any([isinstance(x, Dooder) for x in self])

    @property
    def locations(self):
        return self

    @property
    def coordinates(self):
        return [x.coordinates for x in self]

    @property
    def random(self):
        return random.choice(self)
