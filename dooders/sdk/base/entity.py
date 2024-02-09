from abc import ABC

from dooders.sdk.base.sequence import Sequence
from dooders.sdk.base.vector import Coordinate
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
    _history : Sequence
        History of the entity. See Sequence for more details.

    Methods
    -------
    update() -> None
        Trigger the entity to update its state.

    Properties
    ----------
    position : Coordinate
        Position of the entity
    history : list
        History of the entity
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
    dooders.sdk.core.sequence.Sequence :
        Sequence of states over time. The sequence is stored as a deque, with
        the most recent state at the start of the sequence.
    """

    def __init__(self, settings: dict = None) -> None:
        self.id = seed.id()
        self.settings = settings
        self.created = settings.get("created", 0)
        self.terminated = None
        self.age = 0
        self._position = settings.get("position", (0, 0))
        self._history = Sequence()

    def update(self) -> None:
        """Trigger the entity to update its state."""
        self.age += 1
        self._history.add_state(self.partial_state)

    @property
    def position(self) -> Coordinate:
        """
        Returns
        -------
        Coordinate
            Position of the entity

        See Also
        --------
        dooders.sdk.base.vector.Coordinate :
            A coordinate in the simulation environment. It is a subclass of
            tuple.
        """
        return self._position

    @position.setter
    def position(self, position: tuple) -> None:
        """
        Parameters
        ----------
        position : tuple
            Position of the entity
        """
        self._position = Coordinate(position)

    @property
    def history(self) -> list:
        """
        Returns
        -------
        list
            History of the entity
        """
        return self._history.history

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
        """
        Returns
        -------
        dict
            The partial state of the entity including id, created, age, and position.
        """
        return {
            "id": self.id,
            "created": self.created,
            "terminated": self.terminated,
            "age": self.age,
            "position": self.position,
        }

    @property
    def state(self) -> dict:
        """
        Returns
        -------
        dict
            The full state of the entity including id, created, age, position,
            and history.
        """
        return {
            "id": self.id,
            "created": self.created,
            "terminated": self.terminated,
            "age": self.age,
            "position": self.position,
            "history": self.history,
        }
