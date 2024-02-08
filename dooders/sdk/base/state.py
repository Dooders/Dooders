from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from dooders.sdk.base.coordinate import Coordinate
from dooders.sdk.utils.short_id import seed

if TYPE_CHECKING:
    from dooders.sdk.base.entity import Entity


@dataclass
class BaseState:
    id: str
    name: str = "DefaultState"
    age: int = 0
    position: Coordinate = Coordinate(0, 0)
    rotation: int = 0
    created: int = None  # cycle number
    current: int = None  # cycle number
    terminated: int = None  # cycle number

    def __post_init__(self, cycle_number: int, position: "Coordinate") -> None:
        self.id = seed.id()
        self.name = self.__class__.__name__
        self.created = cycle_number
        self.current = cycle_number
        self.position = position


class State(ABC):
    # dataclasses that have state attributes
    state_list = []

    def __init__(
        self, entity: "Entity", cycle_number: int, position: "Coordinate"
    ) -> None:
        for state_schema in self.state_list:
            for attribute in state_schema(cycle_number, position):
                setattr(entity, attribute[0], attribute[1])

    @abstractmethod
    def update(self) -> None:
        """Trigger the entity to update its state."""
        raise NotImplementedError("Update method not implemented")

    def get_state(self) -> dict:
        """Return the state of the entity."""
        attributes = {}
        for attribute in self.state_list:
            attributes[attribute[0]] = getattr(self, attribute[0])
        return attributes

    def add_to_state(self, state: Any) -> None:
        """Add an state to the state of the entity."""
        if state not in self.state_list:
            self.state_list.append(state)

    def remove_from_state(self, state: Any) -> None:
        """Remove an state from the state of the entity."""
        if state in self.state_list:
            self.state_list.remove(state)

    def get_from_state(self, state: Any) -> None:
        """Get an state from the state of the entity."""
        if state in self.state_list:
            return self.state_list[self.state_list.index(state)]
        else:
            return None
