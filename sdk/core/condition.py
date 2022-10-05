""" 

#! might need to have ability for and/or condition combinations
#! check returns true/false and the probability to check, if needed (ask fate)
"""

from typing import Callable

from sdk.base.base_core import BaseCore


class Condition(BaseCore):
    """ 
    The factory class to be used as a decorator to register a stop condition. 
    """

    # Internal registry for available conditions.
    registry = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """ 
        Register a stop condition.

        Args:
            name: The name of the stop condition.

        Returns:
            The decorator function.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            scope = cls.infer_scope(cls, wrapped_class)
            if scope not in cls.registry:
                cls.registry[scope] = {}
            cls.registry[scope][name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def check_conditions(cls, scope, *args, **kwargs):
        """ 
        Check if any of the registered conditions are met.

        Args:
            simulation: The simulation to check the conditions for.

        Returns:
            True if any of the conditions are met.
        """
        # check in registry in each purpose to see what purpose is the condition from

        for condition in cls.registry[scope]:
            func = cls.registry[scope][condition]
            if func(*args, **kwargs):
                return True, condition
        return False, None
