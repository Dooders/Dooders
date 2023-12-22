from dooders.games.pacman.game import Game
from dooders.games.pacman.models.behavior_tree import BehaviorTree


class Behavior:
    """
    Behavior is what the agent does during the update cycle of the NPC. Takes the input and effects the environment.
    In pacman, the input is the game state, then the behavior decides what to do next, and the environment updates on that.
    Has write privilege/access. Maybe that distinguishes an agent from an entity
    """

    def __init__(self, game: "Game", strategy_type: str = "BehaviorTree") -> None:
        self.game = game
        self.current = self.set_behavior(strategy_type)

    def set_behavior(self, strategy_type):
        if strategy_type == "BehaviorTree":
            return BehaviorTree(self.game)
        elif strategy_type == "FSM":
            return FiniteStateMachine(self.game)
        else:
            raise ValueError("Unknown strategy type")

    def update(self):
        # Delegate the game logic to the selected behavior model
        self.current.run()
