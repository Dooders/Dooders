from typing import TYPE_CHECKING, List, Union

from dooders.games.npc import NPC
from dooders.games.pacman.settings import Colors, Directions, SpawnPositions
from dooders.games.pacman.sprites import PacManSprites
from dooders.games.pacman.states import PacManState
from dooders.games.pacman.targets import PacManTarget
from dooders.sdk.base.coordinate import Coordinate

if TYPE_CHECKING:
    from dooders.games.pacman.game import Game
    from dooders.games.pacman.pellets import Pellet


class PacMan(NPC):
    """
    PacMan is the main character of the game. He is autonomously controlled by
    an AI and must eat all the pellets in the maze while avoiding the ghosts.

    Attributes
    ----------
    color : tuple
        The color of the entity
    alive : bool
        Whether the entity is alive or not
    direction : Coordinate
        The direction the entity is moving in
    sprites : PacManSprites
        The sprites for the entity
    spawn : Coordinate
        The spawn position of the entity
    position : Coordinate
        The current position of the entity
    state : PacManState
        The state of the entity
    previous_position : Coordinate
        The previous position of the entity
    path : List[Coordinate]
        The path the entity to reach its target
    target : PacManTarget
        The target the entity is currently following

    Methods
    -------
    update(game: Game)
        Updates the entity
    eat_pellets(pellet_List: List["Pellet"])
        Checks if the entity has eaten a pellet
    """

    def __init__(self) -> None:
        super().__init__()
        self.color = Colors.YELLOW.value
        self.alive: bool = True
        self.direction = Directions.STOP
        self.sprites = PacManSprites(self)
        self.spawn = Coordinate(SpawnPositions.PACMAN)
        self.position = self.spawn
        self.state = PacManState(self)
        self.previous_position = self.position
        self.path: List[Coordinate] = []
        self.target = PacManTarget()

    def update(self, game: "Game") -> None:
        """
        Updates the Pac-Man's state based on the time delta (dt).

        It handles the movement, checks for overshooting targets, and handles
        portal transitions (like when Pac-Man goes off one side of the screen
        and appears on the other). It also checks for direction reversal.

        Parameters
        ----------
        game : Game
            The game object
        """
        time_delta = game.dt
        self.sprites.update(time_delta)

        if self.alive:
            current_position = self.position.copy()
            self.state.update(game)
            self.target.update(game, self)
            self.find_path(game)
            self.move()
            self.previous_position = current_position

    def eat_pellets(self, pellet_List: List["Pellet"]) -> Union[None, object]:
        """
        Checks for collisions between Pac-Man and any pellet in the provided list.

        If a collision is detected, it returns the pellet that was "eaten".

        Parameters
        ----------
        pellet_List : List["Pellet"]
            A list of pellets to check for collisions with

        Returns
        -------
        Optional[Pellet]
            The pellet that was "eaten" if a collision is detected, None otherwise
        """
        for pellet in pellet_List:
            if self.collide_check(pellet):
                return pellet
        return None
