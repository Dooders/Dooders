""" 
Core: Strategy
--------------
This module contains the strategies used by the simulation.

A strategy is a technique to provide an output. Usually a value or list of values
A collector runs at the end pf each step based on the state at each step
A strategy is an input for a step to process. The strategies will be inputs for different models
A model defines a strategy through a yaml file.
Add a new strategy with the register decorator
"""

from functools import partial
from typing import Any, Callable, Optional

from pydantic import BaseModel

from sdk.core.core import Core


class BaseStrategy(BaseModel):
    # What kind of value needs to be generated
    # Currently Generation or Placement
    Type: str

    # The function generator to be executed
    # Functions are registered from the register decorator
    Func: str

    # Arguments to pass to the StrategyFunc
    Args: Optional[dict] = None

    # The strategy is dependent on the result of another strategy
    # If true, the strategy will be compiled later
    Dependency: Optional[str] = None

    # Used for documentation
    Description: Optional[str] = None

    # This is meant to specify where the strategy is used
    # No functional use. For documentation only
    Used: Optional[str] = None


class Strategy(Core):

    def __init__(self):
        from sdk import strategies

    @classmethod
    def search(cls, function_name: str) -> Any:
        """ 
        Search for a strategy by function name.

        Parameters
        ----------
        function_name : str
            The name of the function to search for.
        """
        components = cls.get_components('sdk.strategies')

        for k, v in components.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 == function_name:
                        return v2
        return None

    @classmethod
    def compile(cls, model: Callable, settings: dict) -> dict:
        """ 
        Compiles a strategy. Method will also add the functions as attributes
        to the model. When the attribute is called, the function will be executed.

        Parameters
        ----------
        model : Callable
            The model to compile the strategy for.
        settings : dict
            The settings for the strategy.
            
        Returns
        -------
        dict
            A dictionary of compiled strategies.
        """
        compiled_strategies = {}

        for name, setting in settings.items():
            component = cls.search(setting.function)
            function = component.function
            args = setting.args

            if component.file_name == 'placement':
                compiled_strategies[name] = partial(
                    function, model.simulation, args)

            else:
                compiled_strategies[name] = partial(function, args)

        for key, value in compiled_strategies.items():
            setattr(model, key, value)

        return compiled_strategies
