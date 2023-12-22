from typing import TYPE_CHECKING

from dooders.games.pacman.models.behavior_tree import BehaviorTree
from dooders.games.pacman.models.finite_state_machine import FiniteStateMachine

if TYPE_CHECKING:
    from dooders.games.pacman.game import Game


class Behavior:
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

    def __init__(self, game: "Game", strategy_type: str = "BehaviorTree") -> None:
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
        self.game = game
        self.model = self.set_behavior(strategy_type)

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
            return BehaviorTree(self.game)
        elif strategy_type in ["FiniteStateMachine", "FSM"]:
            return FiniteStateMachine(self.game)
        else:
            raise ValueError("Unknown strategy type")

    def update(self, game: "Game") -> None:
        """
        Updates the behavior.

        Parameters
        ----------
        game : Game
            The game object
        """
        # Delegate the game logic to the selected behavior model
        if self.alive:
            current_position = self.position.copy()
            self.state.update(game)  # Updates the state
            self.model.run(game)  # Sets the new target
            self.find_path(game)  # Finds the path to the target
            self.move()  # Moves the entity
            self.previous_position = current_position
