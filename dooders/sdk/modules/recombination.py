"""
The Recombination module provides a set of functions designed to emulate the 
process of sexual reproduction in natural systems by recombining the weights of 
two Dooders. The newly combined weights are subsequently inherited by the 
offspring Dooder.

The module currently supports five recombination types:

- `averaging`: Computes the mean of the weights from the parent Dooders.
- `lottery`: Randomly chooses weights from either parent Dooder.
- `crossover`: Selects a random crossover point and integrates the weights of both Dooders.
- `random_range`: Randomly chooses weights within the range defined by the weights of the two parent Dooders.
- `none`: Randomly inherits all weights from one of the parent Dooders, with no recombination involved.
"""

import random

import numpy as np


def averaging_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
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
    >>> averaging_weights(a_weights, b_weights)
    array([3.5, 4.5, 5.5, 6.5, 7.5])
    """
    new_weights = []
    for i in range(len(a_weights)):
        new_weights.append((a_weights[i] + b_weights[i]) / 2)
    return np.array(new_weights)


def lottery_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
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
    >>> random_weights(a_weights, b_weights)
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

    return np.array(new_weights)


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
    >>> crossover_weights(a_weights, b_weights) (crossover point = 3)
    array([1, 2, 3, 9, 10])
    """
    crossover_point = random.randint(0, len(a_weights))
    first_half = a_weights[:crossover_point]
    second_half = b_weights[crossover_point:]
    new_weights = np.concatenate((first_half, second_half), axis=0)
    return new_weights


def random_range_weights(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
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
    >>> random_range_weights(a_weights, b_weights)
    array([3, 4, 4, 8, 9])
    """
    new_weights = []
    for i in range(len(a_weights)):
        random_weight = np.random.uniform(a_weights[i], b_weights[i])
        new_weights.append(random_weight)

    return np.array(new_weights)


RECOMBINATION_TYPES = {
    'averaging': averaging_weights,
    'lottery': lottery_weights,
    'crossover': crossover_weights,
    'random_range': random_range_weights,
    'none': lambda a, b: random.choice([a, b])
}


def recombine(a_weights: np.ndarray,
              b_weights: np.ndarray,
              recombination_type: str = 'averaging') -> np.ndarray:
    """ 
    Recombines the weights of two Dooders to create a new set of weights

    Options for recombination_type: 'averaging', 'lottery', 'crossover', 'random_range', 'none'

    none will randomly select either a or b

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

    if recombination_type not in RECOMBINATION_TYPES:
        raise ValueError(f'Invalid recombination type {recombination_type}.'
                         'Valid options are: "averaging", "lottery", "crossover", "random_range", "none"')
        
    recombined_model_weights = dict.fromkeys(a_weights.keys())
    
    for model in recombined_model_weights.keys():
        
        model_weights_a = a_weights[model]
        model_weights_b = b_weights[model]
    
        recombined_weights = []
        for a, b in zip(model_weights_a.tolist(), model_weights_b.tolist()):
            recombined_weights.append(
                RECOMBINATION_TYPES[recombination_type](a, b))
            
        recombined_model_weights[model] = recombined_weights

    return recombined_model_weights
