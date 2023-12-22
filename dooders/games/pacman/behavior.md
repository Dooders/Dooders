# Behavior Manager Implementation


1. **Initialization with Pre-Game Selection**:
   - The Behavior Manager takes an argument or a setting indicating which behavior model to use.
   - Initialize the selected behavior model based on this pre-game choice.

2. **Single Update Method**:
   - Since the behavior model does not change during the game, the update method only needs to call the `run` or `update` method of the active model.

3. **No Switching Logic Needed**:
   - Since the model is chosen pre-game and remains constant, there's no need for logic to switch models during gameplay.

## Example Code

```python
class BehaviorManager:
    def __init__(self, game, strategy_type):
        self.game = game
        self.current_behavior = self.initialize_behavior(strategy_type)

    def initialize_behavior(self, strategy_type):
        if strategy_type == "BehaviorTree":
            return self.initialize_behavior_tree()
        elif strategy_type == "FSM":
            return self.initialize_fsm()
        else:
            raise ValueError("Unknown strategy type")

    def initialize_behavior_tree(self):
        # Code to initialize the Behavior Tree
        pass

    def initialize_fsm(self):
        # Code to initialize the FSM
        pass

    def update(self):
        # Delegate the game logic to the selected behavior model
        self.current_behavior.run(self.game)
```

## Integration with Game Setup

- Before the game starts, the desired strategy type is selected (could be through a menu, a setting, or developer choice).
- The `BehaviorManager` is then instantiated with this choice, and it sets up the corresponding behavior model.
- During the game, the main game loop or update method simply calls `behavior_manager.update()`, and all the logic is handled by the chosen behavior model.

## Advantages

- **Simplicity**: The manager is simpler since it doesn't need to handle dynamic switching.
- **Performance**: Since there's no need to evaluate conditions to switch models during the game, this approach is more efficient.
- **Clarity**: This setup makes it clear which behavior model is being used, as it's chosen upfront and remains constant.

This approach works well for games where the behavior mode can be predetermined and does not need to adapt to changing game dynamics on the fly. It offers a clear and efficient way to manage different AI strategies.