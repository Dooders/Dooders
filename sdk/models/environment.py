""" 
Environment Model
-----------------
Represents the "physical" environment in which the agents interact.
"""

from random import choices
from typing import TYPE_CHECKING, Any, List

from sdk.base.base_agent import BaseAgent
from sdk.core.surface import Surface

if TYPE_CHECKING:
    from sdk.core.data import UniqueID


GridCell = List[Any]

#! maybe this inherits arena, and arena has the base methods?


class Environment:
    """ 
    Create a new Environment based on the Surface class.

    Methods
    -------
    place_object(object: BaseAgent, position: tuple) -> None
        Place an object at the provided position.
    remove_object(object: BaseAgent) -> None
        Remove an object from the surface.
    move_object(object: BaseAgent, location: tuple) -> None
        Move an object to a new location.
    get_object_types() -> List[BaseAgent]
        Get all object types in the environment.
    get_objects(object_type: str = 'BaseAgent') -> List[BaseAgent]
        Get all objects of a given type.
    get_object(object_id: UniqueID) -> BaseAgent
        Get an object by its id.
    get_random_neighbors(object: BaseAgent, object_type: BaseAgent = 'BaseAgent') -> List[BaseAgent]
        Get all objects in the neighborhood of the given object.
    """

    def __init__(self, settings) -> None:
        """
        Parameters
        ----------
        width: int
            The width of the environment.
        height: int
            The height of the environment.
        torus: bool
            Whether the environment is a torus or not.
        """
        self.surface = Surface.build(settings)

    def place_object(self, object: 'BaseAgent', position: tuple) -> None:
        """
        Place an object at the provided position.

        Parameters
        ----------
        object: BaseAgent
            The object to place.
        position: tuple
            The location to place the object, in the form (x, y).
        """
        location = self.surface[position]
        location.add(object)
        object.position = position
        self.empties.discard(position)

    def remove_object(self, object: 'BaseAgent') -> None:
        """
        Remove an object from the surface object.

        Parameters
        ----------
        object: BaseAgent
            The object to remove.
        """
        location = object.position
        self.surface[location].remove(object)
        if self.surface.is_cell_empty(location):
            self.surface.empties.add(location)
        object.position = None

    def move_object(self, object: 'BaseAgent', location: tuple) -> None:
        """ 
        Move an object to a new location.

        Parameters
        ----------
        object: BaseAgent
            The object to move.
        location: tuple
            The location to move the object to.
        """
        position = self.surface.torus_adj(location)
        self.remove_object(object)
        self.place_object(object, position)
        object.position = position

    def get_object_types(self) -> List[BaseAgent]:
        """
        Get all object types in the environment.

        Returns
        -------
        object_types: List[BaseAgent]
            A list of all object types in the environment.
        """
        #! redo this to use the iterator instead
        object_types = []
        for x in range(self.surface.width):
            for y in range(self.surface.height):
                for obj in self.surface[x, y].contents.values():
                    if obj.name not in object_types:
                        object_types.append(obj.__class__.__name__)
        return object_types

    def get_objects(self, object_type: str = 'BaseAgent') -> List[BaseAgent]:
        """
        Get all objects of a given type.

        Parameters
        ----------
        type: str
            The type of object to get.

        Returns
        -------
        objects: List[BaseAgent]
            A list of all objects of the given type.
        """
        #! do I need this with the method above there?
        if object_type == 'BaseAgent':
            object_type = self.get_object_types()

        objects = []
        for x in range(self.surface.width):
            for y in range(self.surface.height):
                for obj in self.surface[x, y].contents.values():
                    if obj.name in object_type:
                        objects.append(obj)
        return objects

    def get_object(self, object_id: 'UniqueID') -> BaseAgent:
        """
        Get an object by its id.

        Parameters
        ----------
        object_id: UniqueID
            The id of the object. Based on a random short uuid assigned to 
            every object at its creation.

        Returns
        -------
        object: BaseAgent
            The object with the given id.
        """
        for x in range(self.surface.width):
            for y in range(self.surface.height):
                for obj in self.surface[x, y].contents.values():
                    if obj.unique_id == object_id:
                        return obj

        return 'No object found'

    def get_random_neighbors(self,
                             object: 'BaseAgent',
                             object_type: BaseAgent = 'BaseAgent') -> List[BaseAgent]:
        """
        Get all objects in the neighborhood of the given object.

        Parameters
        ----------
        object: BaseAgent
            The object to get the neighborhood of.
        object_type: str
            The type of object to get.

        Returns
        -------
        objects: List[BaseAgent]
            A list of all objects in the neighborhood of the given object.
        """
        #! is this duplicative too?
        if object_type == 'BaseAgent':
            object_type_list = self.get_object_types()
        else:
            object_type_list = [object_type]

        objects = []
        for iter in self.surface.iter_neighbors(object[0].position):
            if iter.name in object_type_list:
                objects.append(iter)
        if len(objects) == 0:
            return 'No objects found'

        return objects

    def get_random_neighborhoods(self, location: tuple, n: int = 1) -> List[GridCell]:
        """
        Get all objects in the neighborhood of the given location.

        Parameters
        ----------
        location: tuple
            The location to get the neighborhood of.
        n: int
            The number of neighborhoods to get.

        Returns
        -------
        random_neighborhoods: List[GridCell]
            A list of all objects in the neighborhood of the given location.
        """

        neighborhoods = self.surface.get_neighborhood(location)

        k = min(n, len(neighborhoods))
        random_neighborhoods = choices(neighborhoods, k=k)

        return random_neighborhoods

    def get_object_count(self, object_type: str = 'BaseAgent') -> int:
        """ 
        Get the number of objects of a given type.

        Parameters
        ----------
        object_type: str
            The type of object to count.

        Returns
        -------
        count: int
            The number of objects of the given type.
        """
        return len(self.get_objects(object_type))
