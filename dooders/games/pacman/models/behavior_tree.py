from abc import ABC, abstractmethod
import random


class TreeNode(ABC):
    @abstractmethod
    def run(self, game):
        """
        Run the node.
        """
        raise NotImplementedError(
            f"run() not implemented for {self.__class__.__name__}"
        )


class ActionNode(TreeNode):
    def __init__(self, action):
        self.action = action

    def run(self, game):
        return self.action(game)


class ConditionNode(TreeNode):
    def __init__(self, condition):
        self.condition = condition

    def run(self, game):
        return self.condition(game)


class SelectorNode(TreeNode):
    def __init__(self, children):
        self.children = children

    def run(self, game):
        for child in self.children:
            if child.run(game):
                return True
        return False


class SequenceNode(TreeNode):
    def __init__(self, children):
        self.children = children

    def run(self, game):
        for child in self.children:
            if not child.run(game):
                return False
        return True


def move_towards_pellet(game):
    # Logic to move towards the nearest pellet
    game.pacman.target.current = game.pacman.closest_pellet(game).coordinates
    print(f" search: {game.pacman.target.current}")

    return True


def move_away_from_ghost(game):
    # Logic to move away from the nearest ghost by finding the farthest point
    #! change to move in opposite direction of ghost instead of farthest point
    nearest_ghost = game.pacman.closest_ghost(game)
    game.pacman.target.current = game.find_farthest_point(nearest_ghost.position)
    print(f" escape: {game.pacman.target.current}")

    return True


def wander(game):
    # Logic to move randomly
    position = game.pacman.position
    neighbors = game.map.graph.nearby_spaces(position)
    game.pacman.target.current = random.choice(neighbors).coordinates
    print(f" wander: {game.pacman.target.current}")

    return True


def is_ghost_nearby(game):
    # Check if a ghost is too close
    nearest_ghost = game.pacman.closest_ghost(game)
    distance = game.pacman.position.distance_to(nearest_ghost.position)

    if distance < 2:
        return True
    else:
        return False


def is_pellet_nearby(game):
    # Check if a pellet is nearby
    nearest_pellet = game.pacman.closest_pellet(game)
    distance = game.pacman.position.distance_to(nearest_pellet.coordinates)

    if distance < 2:
        return True
    else:
        return False


# Constructing the behavior tree
pacman_behavior_tree = SelectorNode(
    [
        SequenceNode(
            [ConditionNode(is_ghost_nearby), ActionNode(move_away_from_ghost)]
        ),
        SequenceNode(
            [ConditionNode(is_pellet_nearby), ActionNode(move_towards_pellet)]
        ),
        ActionNode(wander),
    ]
)


# from abc import ABC, abstractmethod
# import random


# class TreeNode(ABC):
#     @abstractmethod
#     def run(self):
#         """
#         Run the node.
#         """
#         raise NotImplementedError(
#             f"run() not implemented for {self.__class__.__name__}"
#         )


# class ActionNode(TreeNode):
#     def __init__(self, action):
#         self.action = action

#     def run(self):
#         return self.action()


# class ConditionNode(TreeNode):
#     def __init__(self, condition):
#         self.condition = condition

#     def run(self):
#         return self.condition()


# class SelectorNode(TreeNode):
#     def __init__(self, children):
#         self.children = children

#     def run(self):
#         for child in self.children:
#             if child.run():
#                 return True
#         return False


# class SequenceNode(TreeNode):
#     def __init__(self, children):
#         self.children = children

#     def run(self):
#         for child in self.children:
#             if not child.run():
#                 return False
#         return True


# def move_towards_pellet(game):
#     # Logic to move towards the nearest pellet
#     game.pacman.target = game.pacman.closest_pellet()

#     return True


# def move_away_from_ghost(game):
#     # Logic to move away from the nearest ghost by finding the farthest point
#     nearest_ghost = game.pacman.closest_ghost()
#     game.pacman.target = game.find_farthest_point(nearest_ghost.position)

#     return True


# def wander(game):
#     # Logic to move randomly
#     neighbors = game.pacman.position.neighbors()
#     game.pacman.target = random.choice(neighbors)

#     return True


# def is_ghost_nearby(game):
#     # Check if a ghost is too close
#     nearest_ghost = game.pacman.closest_ghost()
#     distance = game.pacman.position.distance(nearest_ghost.position)

#     if distance < 2:
#         return True
#     else:
#         return False


# def is_pellet_nearby(game):
#     # Check if a pellet is nearby
#     nearest_pellet = game.pacman.closest_pellet()
#     distance = game.pacman.position.distance(nearest_pellet.position)

#     if distance < 2:
#         return True
#     else:
#         return False


# pacman_behavior_tree = SelectorNode(
#     [
#         SequenceNode(
#             [ConditionNode(is_ghost_nearby), ActionNode(move_away_from_ghost)]
#         ),
#         SequenceNode(
#             [ConditionNode(is_pellet_nearby), ActionNode(move_towards_pellet)]
#         ),
#         ActionNode(wander),
#     ]
# )
