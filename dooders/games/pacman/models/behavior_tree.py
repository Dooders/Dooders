import random

from dooders.games.pacman.engine.tree_node import *


class BehaviorTree:
    #! Break this out of the below Pacman specific behavior tree and into a generic behavior tree
    """
    A behavior tree for the Pacman agent.

    The behavior tree is a tree of nodes that are run in a specific order.

    The tree is structured as follows:
        SelectorNode
            SequenceNode
                ConditionNode
                ActionNode
            SequenceNode
                ConditionNode
                ActionNode
            ActionNode

    Methods
    -------
    run(game: "Game") -> bool
        Runs the behavior tree.
    move_towards_pellet(game: "Game") -> bool
        Moves towards the nearest pellet.
    move_away_from_ghost(game: "Game") -> bool
        Moves away from the nearest ghost.
    wander(game: "Game") -> bool
        Moves randomly.
    is_ghost_nearby(game: "Game") -> bool
        Checks if a ghost is nearby.
    is_pellet_nearby(game: "Game") -> bool
        Checks if a pellet is nearby.
    """

    def __init__(self):
        self.tree = SelectorNode(
            [
                SequenceNode(
                    [
                        ConditionNode(self.is_ghost_nearby),
                        ActionNode(self.move_away_from_ghost),
                    ]
                ),
                SequenceNode(
                    [
                        ConditionNode(self.is_pellet_nearby),
                        ActionNode(self.move_towards_pellet),
                    ]
                ),
                ActionNode(self.wander),
            ]
        )

    def run(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if the behavior tree ran successfully, False otherwise.
        """
        self.tree.run(game)

    def move_towards_pellet(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if NPC moved towards pellet, False otherwise.
        """
        # Logic to move towards the nearest pellet
        game.pacman.target.current = game.pacman.closest_pellet(game).coordinates
        print(f" search: {game.pacman.target.current}")

        return True

    def move_away_from_ghost(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if NPC moved away from ghost, False otherwise.
        """
        # Logic to move away from the nearest ghost by finding the farthest point
        #! change to move in opposite direction of ghost instead of farthest point
        nearest_ghost = game.pacman.closest_ghost(game)
        game.pacman.target.current = game.find_farthest_point(nearest_ghost.position)
        print(f" escape: {game.pacman.target.current}")

        return True

    def wander(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if NPC moved random adjacent space, False otherwise.
        """
        # Logic to move randomly
        position = game.pacman.position
        neighbors = game.map.graph.nearby_spaces(position)
        game.pacman.target.current = random.choice(neighbors).coordinates
        print(f" wander: {game.pacman.target.current}")

        return True

    def is_ghost_nearby(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if a ghost is nearby, False otherwise.
        """
        # Check if a ghost is too close
        nearest_ghost = game.pacman.closest_ghost(game)
        distance = game.pacman.position.distance_to(nearest_ghost.position)

        if distance < 2:
            return True
        else:
            return False

    def is_pellet_nearby(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if a pellet is nearby, False otherwise.
        """
        # Check if a pellet is nearby
        nearest_pellet = game.pacman.closest_pellet(game)
        distance = game.pacman.position.distance_to(nearest_pellet.coordinates)

        if distance < 2:
            return True
        else:
            return False
