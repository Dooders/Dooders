""" 
Environment Model
-----------------
Represents the "physical" environment in which the agents interact.
"""
from typing import Any, List, Union

from dooders.sdk.base.agent import Agent
from dooders.sdk.core.surface import Surface

GridCell = List[Any]


class Environment:
    """ 
    Create a new Environment based on the Surface class.

    Methods
    -------
    place_object(object: Agent, position: tuple) -> None
        Place an object at the provided position.
    remove_object(object: Agent) -> None
        Remove an object from the surface.
    move_object(object: Agent, location: tuple) -> None
        Move an object to a new location.
    get_object_types() -> List[Agent]
        Get all object types in the environment.
    get_objects(object_type: str = 'Agent') -> List[Agent]
        Get all objects of a given type.
    get_object(object_id: str) -> Agent
        Get an object by its id.
    get_random_neighbors(object: Agent, object_type: Agent = 'Agent') -> List[Agent]
        Get all objects in the perception of the given object.
    """

    def __init__(self, simulation, settings: dict) -> None:
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
        self.settings = settings

    def _setup(self) -> None:
        """ 
        Setup the environment.
        """
        self.surface = Surface.build(self.SurfaceType())

    def place_object(self, object: 'Agent', position: tuple) -> None:
        """
        Place an object at the provided position.

        Parameters
        ----------
        object: Agent
            The object to place.
        position: tuple
            The location to place the object, in the form (x, y).
        """
        self.surface.add(object, position)

    def remove_object(self, object: Union['Agent', str]) -> None:
        """
        Remove an object from the surface object.

        Parameters
        ----------
        object: Union[Agent, str]
            The object to remove. 
            Either the object itself or the object's id.
        """
        self.surface.remove(object)

    def move_object(self, object: 'Agent', location: tuple) -> None:
        """ 
        Move an object to a new location.

        Parameters
        ----------
        object: Agent
            The object to move.
        location: tuple
            The location to move the object to.
        """
        self.remove_object(object)
        self.place_object(object, location)

    def get_objects(self, object_type: str = None) -> List[Agent]:
        """
        Get all objects of a given type.

        Parameters
        ----------
        type: str
            The type of object to get.

        Returns
        -------
        objects: List[Agent]
            A list of all objects of the given type.
        """

        yield from self.surface.contents(object_type)

    def get_object(self, object_id: str) -> Agent:
        """
        Get an object by its id.

        Parameters
        ----------
        object_id: str
            The id of the object. Based on a random short uuid assigned to 
            every object at its creation.

        Returns
        -------
        object: Agent
            The object with the given id.
        """
        return self.surface[object_id]

    def get_object_count(self, object_type: str = 'Agent') -> int:
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
        return len(list(self.get_objects(object_type)))

    def coordinates(self):
        return self.surface.coordinates()

    def spaces(self):
        return self.surface.spaces()

    def nearby_spaces(self, location: tuple):
        return self.surface.nearby_spaces(location)

    def contents(self, location: tuple):
        return self.surface.contents(location)

    # def collect(self) -> dict:
    #     """
    #     Get a dictionary of all objects in the environment.

    #     Returns
    #     -------
    #     collect: dict
    #         A dictionary of all objects in the environment.
    #     """
    #     space_info = {}

    #     for space in self.spaces():
    #         space_coords = str(space.coordinates)
    #         contents_count = len(space.contents)
    #         contents_pattern = space.contents_pattern
    #         space_info[space_coords] = (contents_count, contents_pattern)

    #     return space_info

    @property
    def state(self) -> dict:
        """ 
        Get the state of the environment.

        Returns
        -------
        state: dict
            The state of the environment.
        """
        return self.surface.state
