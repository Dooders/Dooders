from random import choices
from typing import Callable

from scipy.stats import norm, randint

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
def uniform_distribution(low, high):
    return randint.rvs(low=low, high=high)
    
@Strategies.register("Generation")
def normal_distribution(mean, std):
    return norm.rvs(loc=mean, scale=std)
    
@Strategies.register("Generation")
def fixed_value(value):
    return value
    
@Strategies.register("Placement")
def random_location(simulation, number):
    locations = [(loc[1], loc[2]) for loc in simulation.environment.coord_iter()]
    random_locations = choices(locations, k=number)

    return random_locations
