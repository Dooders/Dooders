""" 
Core: Strategy
--------------
This module contains the strategies used by the simulation.

A strategy is a technique to provide an output. Usually a value or list of values

For example: One strategy will provide a value from a uniform distribution,
based on the min and max values provided.

To add a new strategy:
"""

from functools import partial
from typing import Any, Callable

from dooders.sdk.core.core import Core


class Strategy(Core):
    """ 
    This class is used to compile strategies for 
    the supplied model.
    
    Attributes
    ----------
    STRATEGY_MODULE : str
        The module to search for strategies in.

    Methods
    -------
    search(function_name: str) -> Any   
        Search for a strategy by function name.
    compile(model: Callable, settings: dict) -> dict
        Compiles a strategy. Method will also add the functions as attributes
        to the model. When the attribute is called, the function will be executed.
    """

    STRATEGY_MODULE = 'strategy'

    @classmethod
    def search(cls, function_name: str) -> Any:
        """ 
        Search for a strategy by function name.

        Parameters
        ----------
        function_name : str
            The name of the function to search for.

        Returns
        -------
        Any
            The strategy function.
        """
        components = cls.get_components(cls.STRATEGY_MODULE)

        for k, v in components.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 == function_name:
                        return v2
        return None

    @classmethod
    def compile(cls, model: Callable, settings: dict) -> None:
        """ 
        Compiles a strategy. Method will also add the functions as attributes
        to the model. When the attribute is called, the function will be executed.

        The method will:
        1. Search for the strategy based on the supplied settings dict
        2. Compile the strategy as a partial function
        3. Add the strategy to the model as an attribute

        Parameters
        ----------
        model : Callable
            The model to compile the strategy for.
        settings : dict
            The settings for the strategy.
        """
        compiled_strategies = {}

        for name, setting in settings.items():
            component = cls.search(setting.function)
            function = component.function
            args = setting.args
            compiled_strategies[name] = partial(function, model, args)

        for key, value in compiled_strategies.items():
            setattr(model, key, value)

        model.settings = compiled_strategies
