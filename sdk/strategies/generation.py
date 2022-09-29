
from sdk.core.strategy import Strategies

from scipy.stats import norm, randint



@Strategies.register("Generation")
def uniform_distribution(min: int, max: int) -> int:
    """ 
    Generates a random value between the given low and high values. 
    Followings a uniform distribution.

    Args:
        low (int): The lower bound of the distribution.
        high (int): The upper bound of the distribution.

    Returns:
        The generated value.
    """
    return randint.rvs(low=min, high=max)


@Strategies.register("Generation")
def normal_distribution(min: int, max: int, variation: float = None) -> float:
    """ 
    Generates a random value based on the given mean and standard deviation.
    Followings a normal distribution.

    Args:
        mean (int): The mean of the distribution.
        std (int): The standard deviation of the distribution.

    Returns:
        The generated value.
    """

    mean = (max + min) / 2

    if variation is None:
        variation = (max - min) / 8

    return norm.rvs(loc=mean, scale=variation)


@Strategies.register("Generation")
def fixed_value(value: int) -> int:
    """ 
    Returns a fixed value.

    Args:
        value (int): The value to return.
    """
    return value
