from typing import Callable

from sdk import actions


class Actions:

    actions = {}

    @classmethod
    def register(cls) -> Callable:
        """ 
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.actions[wrapped_class.__name__] = wrapped_class

            return wrapped_class

        return inner_wrapper

    def __call__(self, object, action):
        matched_action = self.actions[action]
        action_results = matched_action.execute(object)

        return action_results
