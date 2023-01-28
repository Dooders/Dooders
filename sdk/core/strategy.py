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

from typing import Any, Callable, Optional

import yaml
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
    def load(cls, name: str) -> dict:
        """ 
        Loads a strategy from a YAML file.
        
        Args:
            path: The path to the YAML file.
            
        Returns:
            A dictionary of strategies.
        """
        path = 'sdk/strategies/' + name + '.yml'
        
        with open(path) as f:
            strategy = yaml.load(f, Loader=yaml.FullLoader)

        return strategy

    @classmethod
    def get(cls, strategy: str, scope: str) -> Callable:
        """ 
        Get a strategy from the registry.
        
        Args:
            strategy: The name of the strategy.
            type: The type of the strategy.

        Returns:    
            The strategy class.
        """

        return cls.get_component('sdk.strategies',)
    
    @classmethod
    def compile(cls, model: Any, raw_strategy: Any):
        """ 
        Compiles a strategy.
        
        Args:
            model: The model to compile the strategy for.
            raw_strategy: The raw strategy to compile.
            
        Returns:
            A compiled strategy.
        """
        
        compiled_strategy = {}
        
        for strat_name, strat in raw_strategy.items():
            strategies = cls.get_component('sdk.strategies', strat['Type'])
            func = strategies[strat['Func']].function
            args = strat['Args']
            
            if strat['Type'] == 'placement':
                compiled_strategy[strat_name] = func(
                    model.simulation, compiled_strategy[strat['Dependency']])

            else:
                compiled_strategy[strat_name] = func(**args)

        for key, value in compiled_strategy.items():
            setattr(model, key, value)

        return compiled_strategy

def compile_strategy(model: Any, raw_strategy: Any):
    """ 
    Compiles a strategy.
    
    Args:
        model: The model to compile the strategy for.
        raw_strategy: The raw strategy to compile.
        
    Returns:
        A compiled strategy.
    """
    
    compiled_strategy = {}
    
    for strat_name, strat in raw_strategy.items():
        func = Core.get_func(strat['Func'], strat['Type'])
        args = strat['Args']
        
        if strat['Type'] == 'placement':
            compiled_strategy[strat_name] = func(
                model.simulation, compiled_strategy[strat['Dependency']])

        else:
            compiled_strategy[strat_name] = func(**args)

    for key, value in compiled_strategy.items():
        setattr(model, key, value)

    return compiled_strategy

def recalculate_strategy(strategy, variable):
    #! might need this to recalculate strategies that are dependent on a strategy that changes by user input
    pass
    


#! add a linear increase based on past value and slope to determine delay in increasing probability or score
#! add many different diff equations and distributions

#! how about dooders carry their own nn weights that gets plugged into a gloabal model that the dooders doesnt habe access to???
#! this would essentially serve as the agents model/mapping of reality
#! there could be a societal model too
#! more awareness gives more visibility to rules and facts
#! weights can now be constant for all generations, access to data is variable, which makes value of predictions dependent on awareness
#! awarness can slowly grow as more of society has knowledge of rules and values. This way "ideas" can spread (spatially)
#! each dooder will have the internal model pipeline
#! dooders can share rules and values that they know aboit. sometimes they are wrong and share bad info
#! can i programatically and mechanically create inference from dooder experimemtation or learning from others???
#! the more rule and values I add, the more complexity, and the more imformation a dooder has to adpat to the growing complexity

