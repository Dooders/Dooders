from abc import ABCMeta, abstractmethod
from random import choices
from typing import Callable, Union

from pydantic import BaseModel
from scipy.stats import norm, randint


class BaseStrategy(BaseModel, metaclass=ABCMeta):
    """
    Base class for strategies.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Union[int, float, str]:
        raise NotImplementedError


strategy = {
    'EnergyPerCycle': {'function': 'UniformDistribution', 'args': {'low': 1, 'high': 10}},
    'MaxTotalEnergy': {'function': 'NormalDistribution', 'args': {'mean': 50, 'std': 10}},
    'EnergyLifespan': {'function': 'FixedValue', 'args': {'value': 7}},
    'EnergyPlacement': {'function': 'RandomLocation'}
}


class Strategies:

    strategies = {
        'Generation': {},
        'Placement': {},
    }

    @classmethod
    def register(cls, type) -> Callable:
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
    def get(cls, strategy, type) -> Callable:
        """ 
        Get a collector from the registry.
        Args:
            name: Name of the collector.
            component: Component of the collector.
        Returns:
            The collector.
        """
        return cls.strategies[type][strategy]


@Strategies.register("Generation")
class UniformDistribution(BaseStrategy):
    #! test this
    low: int = 1
    high: int = 10

    def __call__(self) -> int:
        return randint.rvs(low=self.low, high=self.high)
    

@Strategies.register("Generation")
class NormalDistribution(BaseStrategy):
    #! test this
    mean: int = 50
    std: int = 10

    def __call__(self) -> int:
        return norm.rvs(loc=self.mean, scale=self.std)
    
@Strategies.register("Generation")
class FixedValue(BaseStrategy):
    #! test this
    value: int = 7

    def __call__(self) -> int:
        return self.value
    
@Strategies.register("Placement")
class RandomLocation(BaseStrategy):
    #! test this
    def __call__(self, simulation, number) -> list:
        locations = [(loc[1], loc[2])
                     for loc in simulation.environment.coord_iter()]
        random_locations = choices(locations, k=number)

        return random_locations

# class BaseStrategy(BaseModel):
#     " Make this a decorator with the get method "

#     @classmethod
#     def get(cls, strategy):
#         return getattr(cls, strategy)


# class GenerationStrategies(BaseStrategy):
#     Uniform = Strategies.uniform_distribution
#     Normal = Strategies.normal_distribution
#     Fixed = Strategies.fixed_value


# class PlacementStrategies(BaseStrategy):
#     Random = Strategies.random_selection


class Resources:

    def generation_strategy(self, variable):
        strat = strategy[variable]['function']
        func = Strategies.get(strat, 'Generation')
        args = strategy[variable]['args']

        return round(func(**args)[0])

    def placement_strategy(self, simulation, number):
        func = Strategies.get('RandomLocation', 'Placement')
        args = (simulation, number)

        return func(*args)
