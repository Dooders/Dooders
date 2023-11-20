from abc import ABC
import pygame
from pygame.locals import *
from dooders.game.vector import Vector2
from dooders.game.constants import *
from random import randint


class Entity(ABC):
    """
    Abstract base class for all entities in the game.

    Attributes
    ----------
    name : str
        The name of the entity.
    directions : dict
        A dictionary of directions, mapping direction constants to Vector2 objects.
    direction : int
        The current direction of the entity.
    speed : float
        The speed of the entity.
    radius : int
        The radius of the entity.
    collideRadius : int
        The collision radius of the entity.
    color : tuple
        The color of the entity.
    visible : bool
        Whether or not the entity is visible.
    disable_portal : bool
        Whether or not the entity can use portals.
    goal : Vector2
        The goal position of the entity.
    directionMethod : function
        The method used to determine the entity's direction.
    node : Node
        The current node of the entity.
    startNode : Node
        The starting node of the entity.
    target : Node
        The target node of the entity.
    position : Vector2
        The position of the entity.
    image : pygame.Surface
        The image of the entity.

    Methods
    -------
    set_position()
        Sets the entity's position based on its current node's position.
    update(dt)
        Updates the entity's position based on its current direction and speed,
        taking into account the elapsed time (dt).
    valid_direction(direction)
        Checks if the entity can move in the given direction.
    get_new_target(direction)
        Gets the new target node for the entity, based on the given direction.
    over_shot_target()
        Checks if the entity has overshot its target node.
    reverse_direction()
        Reverses the entity's direction.
    opposite_direction(direction)
        Checks if the given direction is the opposite of the entity's current
        direction.
    valid_directions()
        Gets a list of valid directions for the entity.
    random_direction(directions)
        Gets a random direction from the given list of directions.
    goal_direction(directions)
        Gets the direction that is closest to the entity's goal.
    set_start_node(node)
        Sets the entity's starting node.
    set_between_nodes(direction)
        Sets the entity's position between its current node and the node in the
        given direction.
    reset()
        Resets the entity.
    set_speed(speed)
        Sets the entity's speed.
    render(screen)
        Renders the entity.
    """

    def __init__(self) -> None:
        """
        Initializes various attributes for the entity, including its name,
        directions, speed, radius, color, visibility, and other properties.

        Sets the initial direction to "STOP."

        Takes a node as a parameter, representing the starting node of the entity.

        Parameters
        ----------
        node : Node
            The starting node of the entity.
        """
        self.name = None
        self.directions = {
            UP: Vector2(0, -1),
            DOWN: Vector2(0, 1),
            LEFT: Vector2(-1, 0),
            RIGHT: Vector2(1, 0),
            STOP: Vector2(),
        }
        self.direction = STOP
        self.set_speed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.disable_portal = False
        self.goal = None
        self.directionMethod = self.random_direction
        # self.set_start_node(node)
        self.image = None

    def set_position(self) -> None:
        """
        Sets the entity's position based on its current node's position.
        """
        self.position = self.node.position.copy()

    def update(self, game) -> None:
        """
        Updates the entity's position based on its current direction and speed,
        taking into account the elapsed time (dt).

        Checks if the entity has overshot its target node, and if so, updates
        the node and direction.

        If the entity is at a portal, it updates the node to the portal's
        destination node.

        Parameters
        ----------
        dt : float
            The elapsed time since the last update.
        """
        dt = game.dt
        self.position += self.directions[self.direction] * self.speed * dt

        if self.over_shot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.directionMethod(directions)
            if not self.disable_portal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)

            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

    def valid_direction(self, direction: int) -> bool:
        """
        Checks if the entity can move in the given direction.

        Parameters
        ----------
        direction : int
            The direction to check.

        Returns
        -------
        bool
            True if the entity can move in the given direction, False otherwise.
        """
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def targets(self) -> list:
        """
        Returns a list of target nodes for the entity.

        Returns
        -------
        list
            A list of target nodes for the entity.
        """
        #! double check this
        return [x for x in self.node.neighbors if x is not None]

    def get_new_target(self, direction: int) -> "Node":
        """
        Gets the new target node for the entity, based on the given direction.

        For example, if the entity is moving up, the new target node will be the
        node above the entity's current node.

        Parameters
        ----------
        direction : int
            The direction to check.

        Returns
        -------
        Node
            The new target node for the entity.
        """
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def over_shot_target(self) -> bool:
        """
        Checks if the entity has overshot its target node.

        Returns
        -------
        bool
            True if the entity has overshot its target node, False otherwise.
        """
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitude_squared()
            node2Self = vec2.magnitude_squared()
            return node2Self >= node2Target
        return False

    def reverse_direction(self) -> None:
        """
        Reverses the entity's direction.
        """
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction: int) -> bool:
        """
        Checks if the given direction is the opposite of the entity's current
        direction.

        Parameters
        ----------
        direction : int
            The direction to check.

        Returns
        -------
        bool
            True if the given direction is the opposite of the entity's current
            direction, False otherwise.
        """
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def valid_directions(self) -> list:
        """
        Gets a list of valid directions for the entity.

        It checks if the entity can move in each direction, and if so, adds it
        to the list of valid directions.

        If the entity cannot move in any direction, it adds the opposite of its
        current direction to the list of valid directions.

        Returns
        -------
        list
            A list of valid directions for the entity.
        """
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions: list) -> int:
        """
        Gets a random direction from the given list of directions.

        Parameters
        ----------
        directions : list
            The list of directions to choose from.

        Returns
        -------
        int
            A random direction from the given list of directions.
        """
        return directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions: list) -> int:
        """
        Gets the direction that is closest to the entity's goal.

        Parameters
        ----------
        directions : list
            The list of directions to choose from.

        Returns
        -------
        int
            The direction that is closest to the entity's goal.
        """
        distances = []
        for direction in directions:
            vec = (
                self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            )
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]

    # def set_start_node(self, node: "Node") -> None:
    #     """
    #     Sets the entity's starting node.

    #     Parameters
    #     ----------
    #     node : Node
    #         The starting node of the entity.
    #     """
    #     self.node = node
    #     self.startNode = node
    #     self.target = node
    #     self.set_position()

    # def set_between_nodes(self, direction: int) -> None:
    #     """
    #     Sets the entity's position between its current node and the node in the
    #     given direction.

    #     Parameters
    #     ----------
    #     direction : int
    #         The direction to check.
    #     """
    #     if self.node.neighbors[direction] is not None:
    #         self.target = self.node.neighbors[direction]
    #         self.position = (self.node.position + self.target.position) / 2.0

    def reset(self) -> None:
        """
        Resets the entity's state to its initial state, including its starting
        node, direction, speed, and visibility.
        """
        # self.set_start_node(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def set_speed(self, speed: float) -> None:
        """
        Sets the entity's speed based on a given value.

        Parameters
        ----------
        speed : float
            The speed of the entity.
        """
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders the entity on the game screen.

        It either displays an image at the entity's position or draws a circle
        with a specified color and radius.

        Parameters
        ----------
        screen : pygame.Surface
            The game screen.
        """
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.as_tuple())
            else:
                p = self.position.as_int()
                pygame.draw.circle(screen, self.color, p, self.radius)
