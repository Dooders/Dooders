from typing import Any, List

from sdk.base_object import BaseObject
from sdk.environment.base import BaseEnvironment

MultiGridContent = List[Any] #! fix this here and in base


class Environment(BaseEnvironment):

    grid: List[List[MultiGridContent]]

    def __init__(self, params) -> None:
        """
        Create a new MultiGrid object.

        Args:
            width, height: The size of the grid to create.
            torus: Boolean whether the grid wraps or not.
        """
        super().__init__(params)


    def place_object(self, object: object, location: tuple) -> None:
        """
        Place an object at the given location.

        Args:
            object: The object to place.
            location: The location to place the object.
        """
        x, y = location
        if object not in self.grid[x][y]:
            self.grid[x][y].append(object)
        object.position = location
        self.empties.discard(location)

    def remove_object(self, object: object) -> None:
        """
        Remove an object from the grid.

        Args:
            object: The object to remove.
        """
        location = object.position
        x, y = location
        self.grid[x][y].remove(object)
        if self.is_cell_empty(location):
            self.empties.add(location)
        object.position = None

    def move_object(self, object: object, location: tuple) -> None:
        position = self.torus_adj(location)
        self.remove_object(object)
        self.place_object(object, position)
        object.position = position


    def get_objects(self, object_type=BaseObject) -> List[BaseObject]:
        """
        Get all objects of a given type.

        Args:
            type: The type of object to get.
        """

        # object_type_dict = {'BaseObject': BaseObject,
        #                     'Energy': Energy,
        #                     'Dooder': Dooder}

        # object_type_class = object_type_dict[object_type]
  
        objects = []
        for x in range(self.width):
            for y in range(self.height):
                for obj in self.grid[x][y]:
                    if isinstance(obj, object_type):
                        objects.append(obj)
        return objects

    @property
    def object_types(self):
        pass
