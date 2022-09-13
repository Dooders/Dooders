from random import choices
from scipy.stats import randint, norm
from pydantic import BaseModel, Field
from typing import List, Union


# I dont know how to go forward with this. Maybe each base strategy is its
# own class that is called and has a method to regenerate if needed
# make it so whatever strategy is choses it is easily applied by the resources class
# must have a way to pass in the required arguments and a way to identify from config


def get_uniform_rvs(low, high, size=1):
    return randint.rvs(low=low, high=high, loc=0, size=size)


def get_normal_rvs(mean, std, size=1):
    return norm.rvs(loc=mean, scale=std, size=size)

class FixedValue(BaseModel):
    
    @staticmethod
    def generate(value: int):
        return value
    
class UniformDistribution(BaseModel):
    
    @staticmethod
    def generate(low: int, high: int, size: int = 1):
        return get_uniform_rvs(low, high, size)[0]
    
class NormalDistribution(BaseModel):
    
    @staticmethod
    def generate(mean: int, std: int, size: int = 1):
        return round(get_normal_rvs(mean, std, size)[0])
    
class Strategies:
    # make this another plugin for adding strategies easily
    Fixed = FixedValue
    Uniform = UniformDistribution
    Normal = NormalDistribution
    
    @classmethod
    def get(cls, strategy: str):
        return getattr(cls, strategy)
    
    @classmethod
    def get_strategy(cls, strategy: str):
        return cls.get(strategy)
        

# MaxTotalEnergy (None, fixed, dist, dynamic)
# EnergyPerCycle (None, fixed, uniform, dynamic)
# EnergyPlacement (Random, weighted, hotspot)
# EnergyDissipation (None, fixed, uniform)

# class MaxTotalEnergy:
    
#     @staticmethod
#     def get_strategy(strategy: str, **kwargs):
#         return Strategies.get(strategy).generate(**kwargs)

StrategyOptions = {
    'Fixed': {
        'value': 100  
    },
    'Uniform': {
        'low': 0,
        'high': 100
    },
    'Normal': {
        'mean': 50,
        'std': 10
    }
}

options = {
    'value': 100
}

MaxTotalEnergy = Strategies.get_strategy('Fixed')
print(MaxTotalEnergy.generate(**options))

MaxTotalEnergy = Strategies.get_strategy('Uniform')
print(MaxTotalEnergy)

MaxTotalEnergy = Strategies.get_strategy('Normal')
print(MaxTotalEnergy)
    
# print(MaxTotalEnergy.get_strategy('Fixed', value=10))
# print(MaxTotalEnergy.get_strategy('Uniform', low=1, high=10, size=1))
# print(MaxTotalEnergy.get_strategy('Normal', mean=5, std=1, size=1))
# print(MaxTotalEnergy)
print('*****************')
        

class Resources:
    
    @staticmethod
    def get_strategy(self, strategy: str, **kwargs):
        return Strategies.get(strategy).generate(**kwargs)

    def calculate_resources(self, strategy: str) -> int:
        """ Calculate the number of resources based on the strategy 
        Should be a function that return the count of energy for this cycle, 
        based on the strategy provided when the simulation is started
        """
        
        
        if strategy == "uniform":
            return get_uniform_rvs(1, 10)

        elif strategy == "normal":
            return get_normal_rvs(50, 15)

        elif strategy == "fixed":
            return 10

        else:
            return ValueError("Unknown strategy")
            
            
    def calculate_max_energy(self, strategy: str):
        if strategy == "uniform":
            return get_uniform_rvs(1, 10)
        elif strategy == "normal":
            return get_normal_rvs(50, 15)
        elif strategy == "fixed":
            return 10
        else:
            return ValueError("Unknown strategy")
            

    def energy_placement(self, strategy: str):
        energy_count = self.calculate_resources()

        if strategy == "random":
            locations = [(loc[1], loc[2]) for loc in self.environment.coord_iter()]
            random_locations = choices(locations, k=len(energy_count))
            pass
        elif strategy == "weighted":
            pass
        elif strategy == "hotspot":
            pass
