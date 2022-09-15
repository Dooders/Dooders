from random import choices

from pydantic import BaseModel
from scipy.stats import norm, randint

strategy = {
    'EnergyPerCycle': {'function': 'Uniform', 'args': {'low': 1, 'high': 10}},
    'MaxTotalEnergy': {'function': 'Normal', 'args': {'mean': 50, 'std': 10}},
    'EnergyLifespan': {'function': 'Fixed', 'args': {'value': 7}},
    'EnergyPlacement': {'function': 'Random'}
}


class Strategies(BaseModel):

    @staticmethod
    def uniform_distribution(low: int, high: int, size: int = 1):
        return randint.rvs(low=low, high=high, loc=0, size=size)

    @staticmethod
    def normal_distribution(mean: int, std: int, size: int = 1):
        return norm.rvs(loc=mean, scale=std, size=size)

    @staticmethod
    def fixed_value(value):
        return [value]

    @staticmethod
    def random_selection(simulation, number):
        locations = [(loc[1], loc[2])
                     for loc in simulation.environment.coord_iter()]
        random_locations = choices(locations, k=number)

        return random_locations


class BaseStrategy(BaseModel):
    " Make this a decorator with the get method "

    @classmethod
    def get(cls, strategy):
        return getattr(cls, strategy)


class GenerationStrategies(BaseStrategy):
    Uniform = Strategies.uniform_distribution
    Normal = Strategies.normal_distribution
    Fixed = Strategies.fixed_value


class PlacementStrategies(BaseStrategy):
    Random = Strategies.random_selection


class Resources:

    def generation_strategy(self, variable):
        strat = strategy[variable]['function']
        func = GenerationStrategies.get(strat)
        args = strategy[variable]['args']

        return round(func(**args)[0])

    def placement_strategy(self, number):
        pass
