# Game settings
from enum import Enum


class Dimensions:
    TILEWIDTH = 16
    TILEHEIGHT = 16
    NROWS = 36
    NCOLS = 28
    PADDING = 10
    SCREENWIDTH = NCOLS * TILEWIDTH
    SCREENHEIGHT = NROWS * TILEHEIGHT
    SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)
    # SCREENSIZE = SCREENWIDTH + 2 * PADDING, SCREENHEIGHT + 2 * PADDING


class Colors(Enum):
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    PINK = (255, 100, 150)
    TEAL = (100, 255, 255)
    ORANGE = (230, 190, 40)
    GREEN = (0, 255, 0)


class Directions(Enum):
    STOP = 0
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    PORTAL = 3


class GhostStates(Enum):
    SCATTER = 0
    CHASE = 1
    FREIGHT = 2
    SPAWN = 3


class Texts(Enum):
    SCORETXT = 0
    LEVELTXT = 1
    READYTXT = 2
    PAUSETXT = 3
    GAMEOVERTXT = 4
