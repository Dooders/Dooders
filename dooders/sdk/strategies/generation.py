""" 
Strategy: Generation
--------------------
This module contains the strategies for generating the number of resources.
"""

from typing import Callable

from scipy.stats import norm, randint

from dooders.sdk.core.core import Core


@Core.register('strategy')
def uniform_distribution(model: Callable, args: dict) -> int:
    """ 
    Generates a random value between the given low and high values. 
    Followings a uniform distribution.

    Parameters
    ----------
    model : Callable
        The model object that contains the environment, agents, and other models.
    args : dict
        The arguments for the strategy.

    Returns
    -------
    int
        The generated value based on a uniform distribution.
    """
    return randint.rvs(low=args['min'], high=args['max'])


@Core.register('strategy')
def normal_distribution(model: Callable, args: dict) -> float:
    """ 
    Generates a random value based on the given mean and standard deviation.
    Followings a normal distribution.

    Parameters
    ----------
    model : Callable
        The model object that contains the environment, agents, and other models.
    args : dict
        The arguments for the strategy.

    Returns
    -------
    float
        The generated value based on a normal distribution.
    """

    mean = (args['max'] + args['min']) / 2

    if args.get('variation') is None:
        variation = (args['max'] - args['min']) / 8
    else:
        variation = args['variation']

    return norm.rvs(loc=mean, scale=variation)


@Core.register('strategy')
def fixed_value(model: Callable, args: dict) -> int:
    """ 
    Returns a fixed value.

    Parameters
    ----------
    model : Callable
        The model object that contains the environment, agents, and other models.
    args : dict
        The arguments for the strategy.

    Returns
    -------
    int
        The fixed value.
    """
    return args['value']
