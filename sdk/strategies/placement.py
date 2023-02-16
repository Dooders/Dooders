from random import choices
from typing import Callable

from sdk.core import Strategy


@Strategy.register()
def random_location(model: Callable, args: dict) -> list:
    """ 
    Generates a list of locations for the given number of resources 
    and based on the provided strategy.

    Parameters
    ----------
    model : Callable
        The model object that contains the environment, agents, and other models.
    args : dict
        The arguments for the strategy.

    Returns
    -------
    list
        A list of random locations based on the SeedCount.
    """
    #! this takes a list of coordinates, the coordinates are tuples
    locations = [loc for loc in model.simulation.environment.coordinates()]
    random_locations = choices(locations, k=model.SeedCount())

    return random_locations
