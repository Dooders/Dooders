""" 
Strategies
----------

This module contains the strategies used by the simulation.

A strategy is a technique to provide an output. Usually a valueor list of values
A collector runs at the end pf each step based on the state at each step
A strategy is an input for a step to process. The strategies will be inputs for different models
A model defines a strategy through a yaml file.
Add a new strategy with the register deckrator
"""

from random import choices
from typing import TYPE_CHECKING, Any, Callable, Optional

import yaml
from pydantic import BaseModel
from scipy.stats import norm, randint

if TYPE_CHECKING:
    from sdk.simulation import Simulation


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

    # Used for documentstion
    Description: Optional[str] = None

    # This is meant to specifiy where the strategy is used
    # No functional use. For documentstion only
    Used: Optional[str] = None


class Strategies:

    # update for dynamic strategy type dicts
    strategies = {
        'Generation': {},
        'Placement': {},
        'Genetics': {}
    }

    @classmethod
    def load_strategy(cls, path: str) -> dict:
        """ 
        Loads a strategy from a YAML file.
        
        Args:
            path: The path to the YAML file.
            
        Returns:
            A dictionary of strategies.
        """
        with open(path) as f:
            strategy = yaml.load(f, Loader=yaml.FullLoader)

        return strategy

    @classmethod
    def register(cls, type: str) -> Callable:
        """ 
        Register a collector in the registry.
        Args:
            name: Name of the collector.
            component: Component of the collector.
        Returns:
            The decorator function.
        """
        def inner_wrapper(wrapped_class: Callable) -> Callable:
            cls.strategies[type][wrapped_class.__name__] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def get(cls, strategy: str, type: str) -> Callable:
        """ 
        Get a strategy from the registry.
        
        Args:
            strategy: The name of the strategy.
            type: The type of the strategy.

        Returns:    
            The strategy class.
        """
        return cls.strategies[type][strategy]


def compile_strategy(model: Any, raw_strategy: Any) -> dict[BaseStrategy]:
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
        func = Strategies.get(strat['Func'], strat['Type'])
        args = strat['Args']

        if strat['Type'] == 'Placement':
            compiled_strategy[strat_name] = func(
                model.simulation, compiled_strategy[strat['Dependency']])

        else:
            compiled_strategy[strat_name] = func(**args)

    for key, value in compiled_strategy.items():
        setattr(model, key, value)

    return compiled_strategy


#################################
##### Generation Strategies #####
#################################

# @Strategies.register("Generation")
# def uniform_distribution(min: int, max: int) -> int:
#     """ 
#     Generates a random value between the given low and high values. 
#     Followings a uniform distribution.

#     Args:
#         low (int): The lower bound of the distribution.
#         high (int): The upper bound of the distribution.

#     Returns:
#         The generated value.
#     """
#     return randint.rvs(low=min, high=max)


# @Strategies.register("Generation")
# def normal_distribution(min: int, max: int, variation: float = None) -> float:
#     """ 
#     Generates a random value based on the given mean and standard deviation.
#     Followings a normal distribution.

#     Args:
#         mean (int): The mean of the distribution.
#         std (int): The standard deviation of the distribution.

#     Returns:
#         The generated value.
#     """

#     mean = (max + min) / 2

#     if variation is None:
#         variation = (max - min) / 8

#     return norm.rvs(loc=mean, scale=variation)


# @Strategies.register("Generation")
# def fixed_value(value: int) -> int:
#     """ 
#     Returns a fixed value.

#     Args:
#         value (int): The value to return.
#     """
#     return value


# ################################
# ##### Placement Strategies #####
# ################################

# @Strategies.register("Placement")
# def random_location(simulation: 'Simulation', number: int) -> list:
#     """ 
#     Generates a list of locations for the given number of resources and based on the provided strategy.

#     Args:
#         simulation (Simulation): The simulation object.
#         number (int): The number of locations to generate.

#     Returns:
#         A list of locations.
#     """
#     locations = [(loc[1], loc[2])
#                  for loc in simulation.environment.coord_iter()]
#     random_locations = choices(locations, k=number)

#     return random_locations


# ################################
# ###### Genetic Strategies ######
# ################################

# @Strategies.register("Genetics")
# def random_genetics(value: int) -> int:
#     return 'working'


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

