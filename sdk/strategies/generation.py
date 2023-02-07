
from scipy.stats import norm, randint
from sdk.core.strategy import Strategy


@Strategy.register()
def uniform_distribution(args) -> int:
    """ 
    Generates a random value between the given low and high values. 
    Followings a uniform distribution.

    Args:
        low (int): The lower bound of the distribution.
        high (int): The upper bound of the distribution.

    Returns:
        The generated value.
    """
    return randint.rvs(low=args['min'], high=args['max'])


@Strategy.register()
def normal_distribution(args) -> float:
    """ 
    Generates a random value based on the given mean and standard deviation.
    Followings a normal distribution.

    Args:
        mean (int): The mean of the distribution.
        std (int): The standard deviation of the distribution.

    Returns:
        The generated value.
    """

    mean = (args['max'] + args['min']) / 2

    if args.get('variation') is None:
        variation = (args['max'] - args['min']) / 8
    else:
        variation = args['variation']

    return norm.rvs(loc=mean, scale=variation)


@Strategy.register()
def fixed_value(args) -> int:
    """ 
    Returns a fixed value.

    Args:
        value (int): The value to return.
    """
    return args['value']
