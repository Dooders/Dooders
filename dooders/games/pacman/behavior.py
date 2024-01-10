from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from dooders.games.npc import NPC

from dooders.games.pacman.models.behavior_tree import BehaviorTree
from dooders.games.pacman.models.finite_state_machine import PacManFSM, GhostFSM

if TYPE_CHECKING:
    from dooders.games.pacman.game import Game


class Behavior(ABC):
    """
    Behavior is what the agent does during the update cycle of the NPC.

    Takes the input and effects the environment.

    In pacman, the input is the game state, then the behavior decides what to do
    next, and the environment updates on that.

    Has write privilege/access. Maybe that distinguishes an agent from an entity

    Methods
    -------
    set_behavior(strategy_type: str) -> "Behavior"
        Sets the behavior strategy.
    update(game: "Game")
        Runs the behavior logic.
    """

    def __init__(self, npc: "NPC", strategy_type: str = "PacManFSM") -> None:
        """
        Parameters
        ----------
        game : Game
            The game object
        strategy_type : str, optional
            The type of behavior strategy to use, by default "BehaviorTree"

        Raises
        ------
        ValueError
            If the behavior strategy type is unknown
        """
        self.npc = npc
        self.model = self.set_behavior(strategy_type)

    @abstractmethod
    def set_behavior(self, strategy_type: str) -> "Behavior":
        """
        Must include a method to set the behavior strategy which is its own class
        and is the specific logic for the behavior.

        Parameters
        ----------
        strategy_type : str
            The type of behavior strategy to use

        Returns
        -------
        Behavior
            The selected behavior strategy that executes behavior model
        """
        raise NotImplementedError("set_behavior() not implemented")

    def update(self, game: "Game") -> None:
        """
        Handles all the logic for the NPC to behave during its update cycle.

        Including:
        - updating the state
        - updating the target
        - finding the path to the target
        - moving the the target on the path

        Parameters
        ----------
        game : Game
            The game object
        """
        # Delegate the game logic to the selected behavior model
        if self.npc.alive:
            current_position = self.npc.position.copy()
            self.npc.state.update(game)  # Updates the state
            self.model.run(game, self.npc)  # Sets the new target
            self.npc.find_path(game)  # Finds the path to the target
            self.npc.move()  # Moves the entity
            self.previous_position = current_position


class PacManBehavior(Behavior):
    def __init__(self, npc: "NPC", strategy_type: str = "PacManFSM") -> None:
        """
        Parameters
        ----------
        game : Game
            The game object
        strategy_type : str, optional
            The type of behavior strategy to use, by default "PacManFSM"
        """
        super().__init__(npc, strategy_type)

    def set_behavior(self, strategy_type: str) -> "Behavior":
        """
        Sets the behavior strategy.

        Parameters
        ----------
        strategy_type : str
            The type of behavior strategy to use

        Returns
        -------
        Behavior
            The behavior strategy
        """
        if strategy_type in ["BehaviorTree", "BT"]:
            return BehaviorTree()
        elif strategy_type in ["PacManFSM", "P-FSM"]:
            return PacManFSM()
        else:
            raise ValueError("Unknown strategy type")


class GhostBehavior(Behavior):
    def __init__(self, npc: "NPC", strategy_type: str = "GhostFSM") -> None:
        """
        Parameters
        ----------
        game : Game
            The game object
        strategy_type : str, optional
            The type of behavior strategy to use, by default "GhostFSM"
        """
        super().__init__(npc, strategy_type)

    def set_behavior(self, strategy_type: str) -> "Behavior":
        """
        Sets the behavior strategy.

        Parameters
        ----------
        strategy_type : str
            The type of behavior strategy to use

        Returns
        -------
        Behavior
            The behavior strategy
        """
        if strategy_type in ["BehaviorTree", "BT"]:
            return BehaviorTree()
        elif strategy_type in ["GhostFSM", "G-FSM"]:
            return GhostFSM()
        else:
            raise ValueError("Unknown strategy type")
