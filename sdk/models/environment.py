""" 

"""

from random import choices
from typing import TYPE_CHECKING, Any, List

from sdk.base.base_environment import BaseEnvironment
from sdk.base.base_object import BaseObject

if TYPE_CHECKING:
    from sdk.core.data import UniqueID


GridCell = List[Any]


class Environment(BaseEnvironment):
    """ 

    """

    grid: List[List[GridCell]]

    def __init__(self, params: dict) -> None:
        """
        Create a new MultiGrid object.

        Args:
            params: The parameters for the environment.

        Attributes:
            grid: The grid of the environment.
            width: The width of the environment.
            height: The height of the environment.
            torus: Whether the environment is toroidal.
            empties: The empty cells in the environment.
        """
        super().__init__(params)

    def place_object(self, object: 'BaseObject', position) -> None:
        """
        Place an object at the given location.

        Args:
            object: The object to place.
            location: The location to place the object.
        """
        #! Verify this works
        x, y = position
        location = self.grid[x][y]
        location.add(object)
        object.position = position
        self.empties.discard(position)

    def remove_object(self, object: 'BaseObject') -> None:
        """
        Remove an object from the grid.

        Args:
            object: The object to remove.
        """
        #! update this code to remove via new design
        location = object.position
        x, y = location
        self.grid[x][y].remove(object)
        if self.is_cell_empty(location):
            self.empties.add(location)
        object.position = None

    def move_object(self, object: 'BaseObject', location) -> None:
        """ 
        Move an object to a new location.

        Args:
            object: The object to move.
            location: The location to move the object to.
        """
        position = self.torus_adj(location)
        self.remove_object(object)
        self.place_object(object, position)
        object.position = position

    def get_object_types(self) -> List[BaseObject]:
        """
        Get all object types in the environment.

        Returns:
            A list of all object types in the environment.
        """
        object_types = []
        for x in range(self.width):
            for y in range(self.height):
                for obj in self.grid[x][y].contents.values():
                    if obj.name not in object_types:
                        object_types.append(obj.__class__.__name__)
        return object_types

    def get_objects(self, object_type: str = 'BaseObject') -> List[BaseObject]:
        """
        Get all objects of a given type.

        Args:
            type: The type of object to get.

        Returns:
            A list of all objects of the given type.
        """
        if object_type == 'BaseObject':
            object_type = self.get_object_types()

        objects = []
        for x in range(self.width):
            for y in range(self.height):
                for obj in self.grid[x][y].contents.values():
                    if obj.name in object_type:
                        objects.append(obj)
        return objects

    def get_object(self, object_id: 'UniqueID') -> BaseObject:
        """
        Get an object by its id.

        Args:
            object_id: The id of the object. Based on a random short uuid assigned to every object at its creation.

        Returns:
            The object with the given id.
        """
        for x in range(self.width):
            for y in range(self.height):
                for obj in self.grid[x][y].contents.values():
                    if obj.unique_id == object_id:
                        return obj

        return 'No object found'

    def get_random_neighbors(self,
                             object: 'BaseObject',
                             object_type: BaseObject = 'BaseObject') -> List[BaseObject]:
        """
        Get all objects in the neighborhood of the given object.

        Args:
            object: The object to get the neighborhood of.
            object_type: The type of object to get.

        Returns:    
            A list of all objects in the neighborhood of the given object.
        """
        if object_type == 'BaseObject':
            object_type_list = self.get_object_types()
        else:
            object_type_list = [object_type]

        objects = []
        for iter in self.iter_neighbors(object[0].position):
            if iter.name in object_type_list:
                objects.append(iter)
        if len(objects) == 0:
            return 'No objects found'

        return objects

    def get_random_neighborhoods(self, location: 'Location', n: int = 1) -> List['Location']:
        """
        Get all objects in the neighborhood of the given location.

        Args:
            location: The location to get the neighborhood of.
            n: The number of neighborhoods to get.

        Returns:
            A list of all objects in the neighborhood of the given location.
        """

        neighborhoods = self.get_neighborhood(location)

        k = min(n, len(neighborhoods))
        random_neighborhoods = choices(neighborhoods, k=k)

        return random_neighborhoods

    def get_object_count(self, object_type: str = 'BaseObject') -> int:
        return len(self.get_objects(object_type))
