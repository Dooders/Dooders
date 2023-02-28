from random import choices
from typing import Callable

from dooders.sdk.core.core import Core


@Core.register('strategy')
def random_location(model: Callable, *value) -> list:
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
    locations = [loc for loc in model.simulation.environment.coordinates()]
    random_locations = choices(locations, k=value[1])

    return random_locations
