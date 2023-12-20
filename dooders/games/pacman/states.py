from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from dooders.games.pacman.settings import GhostStates, PacManStates

if TYPE_CHECKING:
    from dooders.games.npc import NPC


class State(ABC):
    def __init__(self, npc: "NPC") -> None:
        self.timer = 0
        self.time = None
        self.current = None
        self.npc = npc

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """
        Must have an update method that takes in an NPC and a Game object and
        updates the NPC's state.
        """
        raise NotImplementedError("update() method not implemented")


class GhostState(State):
    """
    Handles the state of the ghost.

    States
    ------
    SCATTER
        Ghost scatter to their respective corners of the maze.
    SPAWN
        Ghost return to their spawn point.
    CHASE
        Ghost chases PacMan
    FREIGHT
        Ghosts are vulnerable and can be eaten by PacMan.

    Methods
    -------
    update(dt)
        Increments the timer by the time delta (dt).
        Checks if the timer has exceeded the duration (time) of the current mode.
        If the current mode is SCATTER, it switches to CHASE mode by calling the
        chase method.
        If the current mode is CHASE, it switches back to SCATTER mode by
        calling the scatter method.
    scatter()
        Sets the mode to SCATTER, defines its duration (time), and resets the timer.
    chase()
        Sets the mode to CHASE, defines its duration (time), and resets the timer.
    spawn()
        Sets the mode to SPAWN only if the current mode is FREIGHT.
    freight()
        Sets the mode to FREIGHT if the current mode is SCATTER or CHASE.
    """

    def __init__(self, npc: "NPC") -> None:
        super().__init__(npc)
        self.scatter()

    def update(self, dt: float) -> None:
        """
        Parameters
        ----------
        dt : float
            Time delta
        """
        self.timer += dt
        if self.timer >= self.time:
            if self.current in [
                GhostStates.SCATTER,
                GhostStates.SPAWN,
                GhostStates.FREIGHT,
            ]:
                self.chase()
            elif self.current is GhostStates.CHASE:
                self.scatter()

        if self.current is GhostStates.SPAWN:
            if self.npc.position == self.npc.spawn:
                self.chase()

    def scatter(self) -> None:
        self.current = GhostStates.SCATTER
        self.time = 7
        self.timer = 0

    def chase(self) -> None:
        self.current = GhostStates.CHASE
        self.time = 20
        self.timer = 0

    def spawn(self) -> None:
        if self.current is GhostStates.FREIGHT:
            self.current = GhostStates.SPAWN

    def freight(self) -> None:
        if self.current in [GhostStates.SCATTER, GhostStates.CHASE]:
            self.timer = 0
            self.time = 7
            self.current = GhostStates.FREIGHT
        elif self.current is GhostStates.FREIGHT:
            self.timer = 0


class PacManState(State):
    """

    The PacMan's state is updated based on the following rules:
    1. If the PacMan is in the search state and a power pellet is nearby,
        then the PacMan moves to the chase state.
    2. If the PacMan is in the search state and a non-vulnerable ghost is
        nearby, then the PacMan moves to the evade state.
    3. If the PacMan is in the chase state and a power pellet is eaten and
        a vulnerable ghost is nearby, then the PacMan moves to the attack
        state.
    4. If the PacMan is in the chase state and a non-vulnerable ghost is
        nearby, then the PacMan moves to the evade state.
    5. If the PacMan is in the attack state and no vulnerable ghosts are
        nearby or a vulnerable ghost is eaten, then the PacMan moves to
        the search state.
    6. If the PacMan is in the evade state and no non-vulnerable ghosts are
        nearby, then the PacMan moves to the search state.
    7. If the PacMan is in the evade state and a power pellet is nearby, then
        the PacMan moves to the chase state.
    """

    def __init__(self, npc: "NPC") -> None:
        super().__init__(npc)
        self.current = PacManStates.SEARCH

    def update(self, game) -> None:
        if self.npc.alive:
            if self.non_vulnerable_ghost_nearby(game):
                self.current = PacManStates.EVADE

            elif self.vulnerable_ghost_nearby(game):
                self.current = PacManStates.CHASE

            else:
                self.current = PacManStates.SEARCH

    def non_vulnerable_ghost_nearby(self, game) -> bool:
        """
        Returns True if a non-vulnerable ghost is nearby, False otherwise.

        Parameters
        ----------
        game : Game
            Game object

        Returns
        -------
        bool
            True if a non-vulnerable ghost is nearby, False otherwise.
        """
        if game.blinky.state.current == GhostStates.CHASE:
            if self.npc.position.distance_to(game.blinky.position) <= 2:
                return True
        return False

    def vulnerable_ghost_nearby(self, game) -> bool:
        """
        Returns True if a vulnerable ghost is nearby, False otherwise.

        Parameters
        ----------
        game : Game
            Game object

        Returns
        -------
        bool
            True if a vulnerable ghost is nearby, False otherwise.
        """
        if game.blinky.state.current == GhostStates.FREIGHT:
            if self.npc.position.distance_to(game.blinky.position) <= 2:
                return True
        return False
