from abc import ABC, abstractmethod

from dooders.sdk.utils.short_id import seed


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
        Unique identifier for the entity
    created : int
        Cycle number when the entity was created
    terminated : int
        Cycle number when the entity was terminated
    position : Coordinate
        Position of the entity
    age : int
        Age of the entity
    _history : list
        History of the entity

    Methods
    -------
    update() -> None
        Trigger the entity to update its state.

    Properties
    ----------
    name : str
        Name of the agent based on the class name
    partial_state : dict
        The partial state of the entity including id, created, age,
        and position.
    state : dict
        The full state of the entity including id, created, age,
        position, and history.

    See Also
    --------
    dooders.sdk.models.dooder.Dooder :
        An Dooder is an entity that can move and interact with the environment
        inside the simulation. It is a subclass of Entity.
    """

    def __init__(self, settings: dict = None) -> None:
        self.id = seed.id()
        self.settings = settings
        self.created = settings.get("created", 0)
        self.terminated = None
        self.position = settings.get("position", (0, 0))
        self.age = 0
        self._history = []  #! bring over the sequence class

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
    def partial_state(self) -> dict:
        """Return the partial state of the entity."""
        return {
            "id": self.id,
            "created": self.created,
            "terminated": self.terminated,
            "age": self.age,
            "position": self.position,
        }

    @property
    def state(self) -> dict:
        """Return the full state of the entity."""
        return {
            "id": self.id,
            "created": self.created,
            "terminated": self.terminated,
            "age": self.age,
            "position": self.position,
            "history": self._history,
        }
