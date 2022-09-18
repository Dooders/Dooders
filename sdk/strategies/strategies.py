""" 
Strategies
----------

This module contains the strategies used by the simulation.
"""

from random import choices
from typing import TYPE_CHECKING, Callable, Optional

from scipy.stats import norm, randint
from pydantic import BaseModel

if TYPE_CHECKING:
    from sdk.simulation import Simulation


class BaseStrategy(BaseModel):
    # What kind of value needs to be generated
    StrategyType: str
    # The function generator to be executed
    StrategyFunc: str
    # Arguments to pass to the StrategyFunc
    Args: Optional[dict] = None
    # The strategy is dependent on the result of another strategy
    # If true, the strategy will be compiled later
    Dependency: Optional[str] = None
    # The result should be refreshed each cycle
    # If true, a generator is returned
    CycleRefresh: Optional[bool] = True
    
    
class Strategies:

    strategies = {
        'Generation': {},
        'Placement': {},
        'Genetics': {}
    }

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

        """
        return cls.strategies[type][strategy]


def compile_strategy(model, raw_strategy):
    compiled_strategy = {}
    strategies = {k:v for k,v in raw_strategy.__dict__.items() if k[:1] != '_'}

    for strat_type, strat in strategies.items():
        print(strat_type, strat)
        func = Strategies.get(strat.Func, strat.Type)
        args = strat.Args

        if strat.Type == 'Generation':
            compiled_strategy[strat_type] = func(**args)

        if strat.Type == 'Placement':
            compiled_strategy[strat_type] = func(
                model.simulation, compiled_strategy['SeedCount'])

        if strat.Type == 'Genetics':
            compiled_strategy[strat_type] = func(1)

    for key, value in compiled_strategy.items():
        setattr(model, key, value)


#################################
##### Generation Strategies #####
#################################

@Strategies.register("Generation")
def uniform_distribution(low: int, high: int) -> int:
    """ 
    Generates a random value between the given low and high values. 
    Followings a uniform distribution.

    Args:
        low (int): The lower bound of the distribution.
        high (int): The upper bound of the distribution.

    Returns:
        The generated value.
    """
    return randint.rvs(low=low, high=high)


@Strategies.register("Generation")
def normal_distribution(mean: int, std: int) -> int:
    """ 
    Generates a random value based on the given mean and standard deviation.
    Followings a normal distribution.

    Args:
        mean (int): The mean of the distribution.
        std (int): The standard deviation of the distribution.

    Returns:
        The generated value.
    """
    return norm.rvs(loc=mean, scale=std)


@Strategies.register("Generation")
def fixed_value(value: int) -> int:
    """ 
    Returns a fixed value.

    Args:
        value (int): The value to return.
    """
    return value


################################
##### Placement Strategies #####
################################

@Strategies.register("Placement")
def random_location(simulation: 'Simulation', number: int) -> list:
    """ 
    Generates a list of locations for the given number of resources and based on the provided strategy.

    Args:
        simulation (Simulation): The simulation object.
        number (int): The number of locations to generate.

    Returns:
        A list of locations.
    """
    locations = [(loc[1], loc[2])
                 for loc in simulation.environment.coord_iter()]
    random_locations = choices(locations, k=number)

    return random_locations


################################
###### Genetic Strategies ######
################################

@Strategies.register("Genetics")
def random_genetics(value: int) -> int:
    return 'working'
