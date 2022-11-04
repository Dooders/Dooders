# looking to consume energy. max or min a goal, like survival days
# base goals: consume energy to maximize cycles, reproduce

from random import choice
from typing import Callable

from sdk.base.base_policy import BasePolicy
from sdk.core.policies import Policies
from sdk.models.energy import Energy


@Policies.register()
class RandomMove(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood
    A neighborhood is all surrounding positions, including the current position

    """

    @classmethod
    def execute(self, dooder) -> tuple:
        neighborhood = dooder.neighborhood
        random_cell = choice(neighborhood)
        
        return random_cell
    
    
@Policies.register()
class RuleBased(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood that has energy.
    A neighborhood is all surrounding positions, including the current position

    """

    @classmethod
    def execute(self, dooder) -> tuple:
        neighbors = dooder.neighbors
        energy = [n for n in neighbors if isinstance(n, Energy)]
        
        if energy:
            energy_positions = [e.position for e in energy]
            random_cell = choice(energy_positions)
            
        else:
            random_cell = dooder.position

        return random_cell
    
    
@Policies.register()
class NeuralNetwork(BasePolicy):
    
    @classmethod
    def execute(self, dooder) -> tuple:
        neighbors = dooder.neighbors
        energy_list = [1 if isinstance(n, Energy) else 0 for n in neighbors]
        
        
    # random, rule-based, NNs
    # maybe new dooders get a product of weights from parents.
    # genetic starting weights, learned weights. get product of that and those weights combine with another dooder during repro
    # genetic weights are a sequence of weights for other activities and policies. all can be contained in single array (with partitions)

    # maybe this recomemds to always be comsuming. it can be base policy that can be overcome/overpowered
    # weights that led to survive longer,
    
# need to make a dataclass for the required output of the policy
# maybe even a dataclass for the input
