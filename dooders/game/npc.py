from abc import ABC, abstractmethod
from dooders.game.constants import Directions
from dooders.sdk.utils.short_id import ShortUUID as short_id

# reset, render, get_path, move

class NPC(ABC):
    def __init__(self) -> None:
        self.seed = short_id()
        self.id = self.seed.uuid()
        self.name = self.__class__.__name__
        self.visible = True
        self.direction = Directions.STOP

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError("update() method not implemented")
