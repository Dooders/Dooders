from random import choices
from scipy.stats import randint, norm
from pydantic import BaseModel
from typing import List


class Strategies(BaseModel):
    # make this another plugin for adding strategies easily
    pass


def get_uniform_rvs(low, high, size=1):
    return randint.rvs(low=low, high=high, loc=0, size=size)


def get_normal_rvs(mean, std, size=1):
    return norm.rvs(loc=mean, scale=std, size=size)


# MaxTotalEnergy (None, static, dist, dynamic)
# EnergyPerCycle (None, static, uniform, dynamic)
# EnergyPlacement (Random, weghted, hotspot)
# EnergyDissapation (None, static, uniform)

class MaxTotalEnergy(BaseModel):
    None: field()
    Static: field()


class Resources:

    def get_energy_count(self, strategy: str) -> int:
        if strategy == "uniform":
            return get_uniform_rvs(1, 10)

        elif strategy == "normal":
            return get_normal_rvs(50, 15)

        elif strategy == "fixed":
            return 10

        else:
            return ValueError("Unknown strategy")

    def energy_placement(self, strategy: str):
        energy_count = self.get_energy_count()

        if strategy == "random":
            locations = [(loc[1], loc[2]) for loc in self.environment.coord_iter()]
            random_locations = choices(locations, k=len(energy_count))
            pass
        elif strategy == "weighted":
            pass
        elif strategy == "hotspot":
            pass
