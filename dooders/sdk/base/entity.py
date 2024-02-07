from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from dooders.sdk.utils import seed

if TYPE_CHECKING:
    from dooders.sdk.base.coordinate import Coordinate


class Entity(ABC):
    """
    Base class for all objects in the simulation environment.

    An entity is an object that exists in the environment of the simulation.

    An entity itself does not interact with the environment, but it has a state
    that can be updated.

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
    dooders.sdk.base.agent.Agent :
        An agent is an entity that can move and interact with the environment
        inside the simulation. It is a subclass of Entity.
    """

    def __init__(self, position: "Coordinate", cycle_number: int) -> None:
        self.id = seed.id()
        self.created = cycle_number
        self.terminated = None
        self.cycle_number = cycle_number
        self.position = position

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
            "cycle_number": self.cycle_number,
            "position": self.position.state,
        }
