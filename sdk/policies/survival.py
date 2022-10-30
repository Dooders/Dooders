# looking to consume energy. max or min a goal, like survival days
# base goals: consume energy to maximize cycles, reproduce

from random import choice
from typing import Callable

from sdk.models.energy import Energy
from sdk.core.policies import Policies
from sdk.base.base_policy import BasePolicy

    # input: needed data, dooder, goal
    # output: action and eval?
    # plugin like
    # get data from Information? -> apply policy to data and goal -> execute action or "recommend" action?
    # should policy just recomemd and not do execution? How to train then? policy waits for result? can i async a task that only continues if something happens?


@Policies.register()
class RandomMove(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood
    A neighborhood is all surrounding positions, including the current position

    """

    __query__ = {'type': 'environment',
                 'information': 'neighborhood'}

    @classmethod
    def execute(self, dooder) -> tuple:
        neighborhood = dooder.neighborhood
        random_cell = choice(neighborhood)
        
        return random_cell

    # random, rule-based, NNs
    # rule example: any location > 0 energy, move and comsume. If multiple, choose random.
    # random example: choose any square, move, consume energy if there.
    # maybe new dooders get a product of weights from parents.
    # genetic starting weights, learned weights. get product of that and those weights combine with another dooder during repro
    # genetic weights are a sequence of weights for other activities and policies. all can be contained in single array (with partitions)

    # maybe this recomemds to always be comsuming. it can be base policy that can be overcome/overpowered
    # weights that led to survive longer,
    
# need to make a dataclass for the required output of the policy
# maybe even a dataclass for the input
