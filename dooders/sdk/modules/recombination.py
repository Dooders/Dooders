import random
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from dooders.sdk.models.dooder import Dooder


def average_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
    """ 
    Averages the weights of two Dooders to create a new set of weights

    Parameters
    ----------  
    a_weights : (np.ndarray)
        The weights of the first Dooder
    b_weights : (np.ndarray)
        The weights of the second Dooder

    Returns
    -------
    new_weights : (np.ndarray)

    Examples
    --------
    >>> a_weights = np.array([1, 2, 3, 4, 5])
    >>> b_weights = np.array([6, 7, 8, 9, 10])
    >>> average(a_weights, b_weights)
    array([3.5, 4.5, 5.5, 6.5, 7.5])
    """
    new_weights = []
    for i in range(len(a_weights)):
        new_weights.append((a_weights[i] + b_weights[i]) / 2)
    return new_weights


def random_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
    """ 
    Randomly selects weights between the range of the two Dooders 
    to create a new set of weights

    Parameters
    ----------
    a_weights : (np.ndarray)
        The weights of the first Dooder
    b_weights : (np.ndarray)
        The weights of the second Dooder

    Returns
    -------
    new_weights : (np.ndarray)

    Examples
    --------
    >>> a_weights = np.array([1, 2, 3, 4, 5])
    >>> b_weights = np.array([6, 7, 8, 9, 10])
    >>> random(a_weights, b_weights)
    array([1, 7, 8, 4, 5])
    """
    new_weights = []
    for i in range(len(a_weights)):
        # Perform crossover at the gene level
        geneA = a_weights[i]
        geneB = b_weights[i]

        # Randomly select a gene from either parent
        crossed_gene = random.choice([geneA, geneB])

        new_weights.append(crossed_gene)

    return new_weights


def crossover_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
    """ 
    Creates a new set of weights based on a random crossover point 
    between the two Dooders weights

    Parameters
    ----------
    a_weights : (np.ndarray)
        The weights of the first Dooder
    b_weights : (np.ndarray)
        The weights of the second Dooder

    Returns
    -------
    new_weights : (np.ndarray)

    Examples
    --------
    >>> a_weights = np.array([1, 2, 3, 4, 5])
    >>> b_weights = np.array([6, 7, 8, 9, 10])
    >>> crossover(a_weights, b_weights) (crossover point = 3)
    array([1, 2, 3, 9, 10])
    """
    crossover_point = random.randint(0, len(a_weights))
    first_half = a_weights[:crossover_point]
    second_half = b_weights[crossover_point:]
    new_weights = first_half + second_half
    return new_weights


def range_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
    """ 
    Randomly selects weights between the range of the two Dooders 
    to create a new set of weights

    Parameters
    ----------
    a_weights : (np.ndarray)
        The weights of the first Dooder
    b_weights : (np.ndarray)
        The weights of the second Dooder

    Returns
    -------
    new_weights : (np.ndarray)

    Examples
    --------
    >>> a_weights = np.array([1, 2, 3, 4, 5])
    >>> b_weights = np.array([6, 7, 8, 9, 10])
    >>> range_weights(a_weights, b_weights)
    array([3, 4, 4, 8, 9])
    """
    new_weights = []
    for i in range(len(a_weights)):
        random_weight = np.random.uniform(a_weights[i], b_weights[i])
        new_weights.append(random_weight)

    return new_weights


RECOMBINATION_TYPES = {
    'average': average_weights,
    'random': random_weights,
    'crossover': crossover_weights,
    'range': range_weights
}


def recombine(a_weights: np.ndarray,
              b_weights: np.ndarray,
              recombination_type: str = 'average') -> np.ndarray:
    """ 
    Recombines the weights of two Dooders to create a new set of weights

    Parameters
    ----------
    a_weights : (np.ndarray)
        The weights of the first Dooder
    b_weights : (np.ndarray)
        The weights of the second Dooder

    Returns
    -------
    new_weights : (np.ndarray)
    """

    return RECOMBINATION_TYPES[recombination_type](a_weights, b_weights)
