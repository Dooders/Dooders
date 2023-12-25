from abc import ABC, abstractmethod

from dooders.sdk.base.state import State


class Entity(ABC):
    def __init__(self, cycle_number, position) -> None:
        self.state = State(self, cycle_number, position)

    @abstractmethod
    def update(self) -> None:
        """Trigger the entity to update its state."""
        raise NotImplementedError("Update method not implemented")

    @property
    def state(self) -> dict:
        """Return the state of the entity."""
        return self.state.get_state()
