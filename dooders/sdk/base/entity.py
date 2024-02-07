from abc import ABC, abstractmethod

from dooders.sdk.utils import seed

DEFAULT_SETTINGS = {"position": (0, 0), "created": 0, "age": 0}


class Entity(ABC):
    """
    Base class for all objects in the simulation environment.

    An entity is an object that exists in the environment of the simulation.

    An entity itself does not interact with the environment, but it can be acted
    upon and has its own state.

    Parameters
    ----------
    position : Coordinate
        Position of the entity, default (0, 0)
    cycle_number : int
        Cycle number of the simulation when the entity is created

    Attributes
    ----------
    id : str
        Unique identifier of the entity
    created : int
        Cycle number of the simulation when the entity is created
    terminated : int
        Cycle number of the simulation when the entity is terminated, default None
    cycle_number : int
        Current cycle number of the simulation
    position : Coordinate
        Position of the entity

    Methods
    -------
    update() -> None
        Trigger the entity to update its state.

    Properties
    ----------
    name : str
        Name of the agent based on the class name
    state : dict
        The state of the entity including id, created, current, and position.

    See Also
    --------
    dooders.sdk.models.dooder.Dooder :
        An Dooder is an entity that can move and interact with the environment
        inside the simulation. It is a subclass of Entity.
    """

    def __init__(self, settings: dict = None) -> None:
        self.id = seed.id()
        self.terminated = None
        self._history = []  #! bring over the sequence class

        if settings is None:
            settings = DEFAULT_SETTINGS

        for key, value in settings.items():
            setattr(self, key, value)

    @abstractmethod
    def update(self) -> None:
        """Trigger the entity to update its state."""
        raise NotImplementedError("Update method not implemented")

    @property
    def name(self) -> str:
        """
        Returns
        -------
        str
            Name of the agent based on the class name
        """
        return self.__class__.__name__

    @property
    def state(self) -> dict:
        """Return the state of the entity."""
        return {
            "id": self.id,
            "created": self.created,
            "terminated": self.terminated,
            "age": self.age,
            "position": self.position,
        }
