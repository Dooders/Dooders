from typing import TYPE_CHECKING

from dooders.game.constants import *

if TYPE_CHECKING:
    from entity import Entity


class MainMode:
    """
    This class provides a structured way to manage and switch between the two
    primary behavior modes of ghosts.

    The ghosts "scatter" to their respective corners of the maze during the
    SCATTER mode and actively chase Pac-Man during the CHASE mode.

    The switching between these modes at regular intervals adds complexity to
    the game and makes the ghost behaviors less predictable.

    Attributes
    ----------
    mode : int
        Current mode of the ghosts
    timer : float
        Time elapsed in the current mode
    time : float
        Duration of the current mode

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
    """

    def __init__(self) -> None:
        """
        Initializes a timer (timer) to track the time elapsed in the current mode.

        Calls the scatter method to set the initial mode to SCATTER.
        """
        self.timer = 0
        self.scatter()

    def update(self, dt: float) -> None:
        """
        Increments the timer by the time delta (dt).

        Checks if the timer has exceeded the duration (time) of the current mode.

        If the current mode is SCATTER, it switches to CHASE mode by calling the
        chase method.

        If the current mode is CHASE, it switches back to SCATTER mode by
        calling the scatter method.

        Parameters
        ----------
        dt : float
            Time delta
        """
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self) -> None:
        """
        Sets the mode to SCATTER, defines its duration (time), and resets the timer.
        """
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self) -> None:
        """
        Sets the mode to CHASE, defines its duration (time), and resets the timer.
        """
        self.mode = CHASE
        self.time = 20
        self.timer = 0


class ModeController:
    """
    The ModeController class provides a more comprehensive way to manage the
    various behavior modes of an entity.

    By introducing additional modes and providing methods to switch between
    them, it allows for more complex and varied behaviors in the game.

    Attributes
    ----------
    timer : float
        Time elapsed in the current mode
    time : float
        Duration of the current mode
    mainmode : MainMode
        MainMode object to manage the primary SCATTER and CHASE modes
    current : int
        Current mode of the entity
    entity : Entity
        Entity to control

    Methods
    -------
    update(dt)
        Updates the MainMode object.
        If the current mode is FREIGHT, it increments the timer and checks if
            the mode's duration has been exceeded. If so, it switches the entity
            back to its normal mode (SCATTER or CHASE).
        If the current mode is either SCATTER or CHASE, it updates the mode based
            on the MainMode object.
        If the current mode is SPAWN, it checks if the entity has reached its
            spawn node. If so, it switches the entity back to its normal mode.
    set_freight_mode()
        Sets the mode to FREIGHT.
        If the entity is already in FREIGHT mode, it resets the timer.
    set_spawn_mode()
        Sets the mode to SPAWN if the current mode is FREIGHT.
    """

    def __init__(self, entity: "Entity") -> None:
        """
        Initializes a timer (timer) to track the time elapsed in the current mode.

        Initializes the MainMode object to manage the primary SCATTER and CHASE modes.

        Sets the initial mode (current) to the mode of the MainMode object.

        Stores a reference to the entity (likely a ghost) that this ModeController
        will control.

        Parameters
        ----------
        entity : Entity
            Entity to control
        """
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self, dt: float) -> None:
        """
        Updates the MainMode object.

        If the current mode is FREIGHT, it increments the timer and checks if
            the mode's duration has been exceeded. If so, it switches the entity
            back to its normal mode (SCATTER or CHASE).
        If the current mode is either SCATTER or CHASE, it updates the mode based
            on the MainMode object.
        If the current mode is SPAWN, it checks if the entity has reached its
            spawn node. If so, it switches the entity back to its normal mode.

        Parameters
        ----------
        dt : float
            Time delta
        """
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                # self.entity.normal_mode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.entity.position == self.entity.spawn:
                self.entity.normal_mode()
                self.current = self.mainmode.mode

    def set_freight_mode(self) -> None:
        """
        Sets the mode to FREIGHT.

        If the entity is already in FREIGHT mode, it resets the timer.
        """
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def set_spawn_mode(self) -> None:
        """
        Sets the mode to SPAWN if the current mode is FREIGHT.
        """
        if self.current is FREIGHT:
            self.current = SPAWN
