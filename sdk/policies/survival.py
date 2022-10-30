# looking to consume energy. max or min a goal, like survival days
# base goals: consume energy to maximize cycles, reproduce

from typing import Callable


class Survival:
    # input: needed data, dooder, goal
    # output: action and eval?
    # plugin like
    # get data from Information? -> apply policy to data and goal -> execute action or "recommend" action?
    # should policy just recomemd and not do execution? How to train then? policy waits for result? can i async a task that only continues if something happens?

    policies = {}

    @classmethod
    def register(cls) -> Callable:
        """ 

        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.policies[wrapped_class.__name__] = wrapped_class

            return wrapped_class

        return inner_wrapper

    @classmethod
    def execute(policy):
        """ 

        """
        pass


@Survival.register()
class RandomMove:
    """ 

    """

    __query__ = {'type': 'environment',
                 'information': 'neighborhood'}

    def __init__(self):
        pass

    def execute(self, dooder):
        pass

    # random, rule-based, NNs
    # rule example: any location > 0 energy, move and comsume. If multiple, choose random.
    # random example: choose any square, move, consume energy if there.
    # maybe new dooders get a product of weights from parents.
    # genetic starting weights, learned weights. get product of that and those weights combine with another dooder during repro
    # genetic weights are a sequence of weights for other activities and policies. all can be contained in single array (with partitions)

    # maybe this recomemds to always be comsuming. it can be base policy that can be overcome/overpowered
    # weights that led to survive longer,
