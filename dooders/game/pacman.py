import random
from typing import Union
import pygame
from pygame.locals import *
from dooders.game.constants import *
from dooders.game.entity import Entity
from dooders.game.sprites import PacManSprites
from dooders.sdk.base.coordinate import Coordinate


# MOVEMENTS = {
#     "UP": Coordinate(0, -TILEWIDTH),
#     "DOWN": Coordinate(0, TILEWIDTH),
#     "LEFT": Coordinate(-TILEWIDTH, 0),
#     "RIGHT": Coordinate(TILEWIDTH, 0),
#     "STOP": Coordinate(0, 0),
# }


class PacMan(Entity):
    """
    PacMan class

    PacMan is the main character of the game. He is controlled by the player
    and must eat all the pellets in the maze while avoiding the ghosts.

    Attributes
    ----------
    name : string
        The name of the entity
    color : tuple
        The color of the entity
    direction : int
        The direction the entity is moving
    alive : bool
        Whether or not the entity is alive
    sprites : PacManSprites
        The sprites for the entity

    Methods
    -------
    reset()
        Resets the entity
    die()
        Kills the entity
    update(dt)
        Updates the entity
    get_valid_key()
        Gets the key pressed by the player
    eat_pellets(pellet_List)
        Checks if the entity has eaten a pellet
    collide_ghost(ghost)
        Checks if the entity has collided with a ghost
    collide_check(other)
        Checks if the entity has collided with another entity
    """

    def __init__(self) -> None:
        Entity.__init__(self)
        self.name = PACMAN
        self.color = YELLOW
        self.alive = True
        self.sprites = PacManSprites(self)
        self.position = Coordinate(13, 26)
        self.brain = FiniteStateMachine()

    def reset(self) -> None:
        """
        Resets the Pac-Man to its initial state, facing left and alive.
        It also resets its sprites.
        """
        Entity.reset(self)
        self.set_between_nodes(LEFT)
        self.alive = True
        self.image = self.sprites.get_start_image()
        self.sprites.reset()

    def die(self) -> None:
        """
        Sets the Pac-Man's state to dead and stops its movement.
        """
        self.alive = False

    def update(self, game) -> None:
        """
        Updates the Pac-Man's state based on the time delta (dt).

        It handles the movement, checks for overshooting targets, and handles
        portal transitions (like when Pac-Man goes off one side of the screen
        and appears on the other). It also checks for direction reversal.

        Parameters
        ----------
        dt : float
            The time delta
        """
        dt = game.dt
        self.sprites.update(dt)

        next_position = self.logic(game)
        if next_position is not None:
            self.move(game, next_position)

    def logic(self, game) -> None:
        next_position = self.brain.update(game, self)

        return next_position

    def move(self, game, coordinate: "Coordinate") -> None:
        self.position = coordinate

    def eat_pellets(self, pellet_List: list) -> Union[None, object]:
        """
        Checks for collisions between Pac-Man and any pellet in the provided list.

        If a collision is detected, it returns the pellet that was "eaten".

        Parameters
        ----------
        pellet_List : list
            A list of pellets to check for collisions with

        Returns
        -------
        object
            The pellet that was "eaten" if a collision is detected, None otherwise
        """
        for pellet in pellet_List:
            if self.collide_check(pellet):
                return pellet
        return None

    def collide_ghost(self, ghost: "Ghost") -> bool:
        """
        Checks if Pac-Man has collided with a ghost.

        Returns True if a collision is detected, False otherwise.

        Parameters
        ----------
        ghost : Ghost
            The ghost to check for collisions with

        Returns
        -------
        bool
            True if a collision is detected, False otherwise
        """
        return self.collide_check(ghost)

    def collide_check(self, other: "object") -> bool:
        """

        Returns True if a collision is detected, False otherwise.

        Parameters
        ----------
        other : object
            The entity to check for collisions with

        Returns
        -------
        bool
            True if a collision is detected, False otherwise
        """
        return self.position == other.position

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                x, y = self.position.as_pixel()
                position = (x - TILEWIDTH / 2, y - TILEHEIGHT / 2)
                screen.blit(self.image, position)
            else:
                raise Exception("No image for PacMan")


class FiniteStateMachine:
    def __init__(self):
        self.state = "Search"
        self.environment = None

    def update(self, game, agent):
        """
        While in the seek pellets state, Ms Pac-Man moves randomly up until it
        detects a pellet and then follows a pathfinding algorithm to eat as many
        pellets as possible and as soon as possible.

        If a power pill is eaten, then Ms PacMan moves to the chase ghosts state
        in which it can use any tree-search algorithm to chase the blue ghosts.

        When the ghosts start flashing, Ms Pac-Man moves to the evade ghosts
        state in which it uses tree search to evade ghosts so that none is
        visible within a distance; when that happens Ms Pac-Man moves back to
        the seek pellets state.

        States
        -------
        """
        # self.update_state(game, agent)
        next_position = self.update_direction(game, agent)

        return next_position

    def update_state(self, game, agent) -> None:
        """
        Update the PacMan's state based on the current game environment.

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

        if self.state == "Search":
            if self.power_pellet_nearby(game, agent):
                self.state = "Chase"
            elif self.non_vulnerable_ghost_nearby(game, agent):
                self.state = "Evade"

        elif self.state == "Chase":
            if self.ate_power_pellet(game, agent) and self.vulnerable_ghost_nearby(
                game, agent
            ):
                self.state = "Attack"
            elif self.non_vulnerable_ghost_nearby(game, agent):
                self.state = "Evade"

        elif self.state == "Attack":
            if not self.vulnerable_ghost_nearby(
                game, agent
            ) or self.ate_vulnerable_ghost(game, agent):
                self.state = "Search"

        elif self.state == "Evade":
            if not self.non_vulnerable_ghost_nearby(game, agent):
                self.state = "Search"
            elif self.power_pellet_nearby(game, agent):
                self.state = "Chase"

    def update_direction(self, game, agent):
        if self.state == "Search":
            next_position = self.search(game, agent)
        elif self.state == "Chase":
            pass
        elif self.state == "Attack":
            pass
        elif self.state == "Evade":
            pass

        return next_position

    def search(self, game, agent):
        """
        Get the next direction to move in the search state.

        If no pellets are nearby, then move randomly.
        If a pellet is nearby, then move towards it.
        """
        #! remove Pellet from space after eaten (or set as eaten)
        neighbor_spaces = game.graph.get_neighbor_spaces(
            agent.position
        )  #! remove get from method name
        pellets = [
            space
            for space in neighbor_spaces
            if space.has("Pellet")
            or space.has("PowerPellet")  #! allow to take list of objects
        ]

        eligible_neighbors = [
            space
            for space in neighbor_spaces
            if space.playable and space not in pellets
        ]

        if len(pellets) >= 1:
            random_space = random.choice(pellets)

        else:
            random_space = random.choice(eligible_neighbors)

        return random_space.coordinates

    def pellet_nearby(self):
        """
        Checks the direct up, down, left, and right cells for power pellets.

        Parameters
        ----------
        environment : dict
            The game environment

        Returns
        -------
        bool
            True if a power pellet is found, False otherwise
        """
        pacman_x, pacman_y = self.position

    def power_pellet_nearby(self, pacman_position, game_board, threshold_distance=3):
        """
        Check if a power pellet is nearby Pac-Man.

        It is considered nearby if it is within a Manhattan distance of
        threshold_distance.

        Manhattan distance is the distance between two points measured along
        the path and not the straight line distance.

        Parameters
        ----------
        pacman_position : tuple

        """
        pacman_x, pacman_y = pacman_position

        # Iterate over the game board
        for y in range(len(game_board)):
            for x in range(len(game_board[y])):
                # Check if the current cell contains a power pellet
                if game_board[y][x] == "POWER_PELLET":
                    # Calculate the Manhattan distance between Pac-Man and the power pellet
                    distance = abs(pacman_x - x) + abs(pacman_y - y)
                    if distance <= threshold_distance:
                        return True

        return False

    def non_vulnerable_ghost_nearby(self, environment):
        return False

    def vulnerable_ghost_nearby(self, environment):
        return False

    def ate_power_pellet(self, environment):
        return False

    def ate_vulnerable_ghost(self, environment):
        return False

    def move_towards_nearest_pellet(self, environment):
        # Search algo for nearest pellet in 4 directions (up, down, left, right)
        # stops when it hits a wall or a pellet, returns distance, shortest distance is chosen
        # get the N spaces in a provided direction
        return None

    def move_towards_power_pellet(self):
        return None

    def move_towards_vulnerable_ghost(self):
        return None

    def move_away_from_ghost(self):
        return None
