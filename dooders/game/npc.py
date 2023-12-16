from dooders.game.constants import Directions
from dooders.sdk.utils.short_id import ShortUUID as short_id


class NPC:
    def __init__(self) -> None:
        self.seed = short_id()
        self.id = self.seed.uuid()
        self.name = None
        self.visible = True
        self.direction = Directions.STOP
