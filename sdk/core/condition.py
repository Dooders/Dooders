""" 
Core: Condition
---------------
This module contains the Condition class,
which is used to register and check conditions.
"""

from typing import Callable

from sdk.base.base_core import BaseCore


class Condition(BaseCore):
    """ 
    The factory class to be used as a decorator to register a stop condition.
    
    Methods
    -------
    register
        Registers a stop condition to the Condition class.
    check_conditions
        Checks if any of the registered conditions are met. 
    """

    # Internal registry for available conditions.
    registry = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """ 
        Register a stop condition.

        Parameters
        ----------
        name: str
            The name of the stop condition.

        Returns
        -------
        inner_wrapper: Callable
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
    def check_conditions(cls, scope: str, *args, **kwargs) -> bool:
        """ 
        Check if any of the registered conditions are met.

        Parameters
        ----------
        simulation: Simulation
            The simulation to check the conditions for.

        Returns
        -------
        bool
            True if any of the conditions are met.
        """
        for condition in cls.registry[scope]:
            func = cls.registry[scope][condition]
            if func(*args, **kwargs):
                return True, condition
        return False, None
