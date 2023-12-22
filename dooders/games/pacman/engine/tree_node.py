from abc import ABC, abstractmethod
from typing import List

from dooders.games.pacman.game import Game


class TreeNode(ABC):
    """
    Abstract base class for tree nodes.

    A tree node is a single node in a behavior tree. It can be either a leaf node
    or a composite node.

    All tree nodes must implement a run() method.

    A leaf node is a node that has no children. It is either an action node or a
    condition node.

    An action node is a node that performs an action. It is a leaf node.

    A condition node is a node that checks a condition. It is a leaf node.

    A composite node is a node that has children. It is either a selector node or
    a sequence node.

    A selector node is a node that runs its children until one of them returns
    True. It is a composite node.

    A sequence node is a node that runs its children until one of them returns
    False. It is a composite node.

    Methods
    -------
    run(game)
        Run the node based on the game state.
    """

    @abstractmethod
    def run(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            The result of the node.
        """
        raise NotImplementedError(
            f"run() not implemented for {self.__class__.__name__}"
        )


class ActionNode(TreeNode):
    """
    A leaf node that performs an action.
    """

    def __init__(self, action: callable) -> None:
        """
        Parameters
        ----------
        action : callable
            The action to perform.
        """
        self.action = action

    def run(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            The result of the action.
        """
        return self.action(game)


class ConditionNode(TreeNode):
    """
    A leaf node that checks a condition.
    """

    def __init__(self, condition: bool) -> None:
        """
        Parameters
        ----------
        condition : bool
            The condition to check.
        """
        self.condition = condition

    def run(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            The result of the condition.
        """
        return self.condition(game)


class SelectorNode(TreeNode):
    """
    A composite node that runs its children until one of them returns True.
    """

    def __init__(self, children: List[TreeNode]) -> None:
        """
        Parameters
        ----------
        children : List[TreeNode]
            The children of the node.
        """
        self.children = children

    def run(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if one of the children returns True, False otherwise.
        """
        for child in self.children:
            if child.run(game):
                return True
        return False


class SequenceNode(TreeNode):
    """
    A composite node that runs its children until one of them returns False.
    """

    def __init__(self, children: List[TreeNode]) -> None:
        """
        Parameters
        ----------
        children : List[TreeNode]
            The children of the node.
        """
        self.children = children

    def run(self, game: "Game") -> bool:
        """
        Parameters
        ----------
        game : Game
            The game state.

        Returns
        -------
        bool
            True if all of the children return True, False otherwise.
        """
        for child in self.children:
            if not child.run(game):
                return False
        return True
