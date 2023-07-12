""" 
Reproduction Policies
---------------------
Policies that are used to create new Dooders from two existing Dooders.
"""

from typing import TYPE_CHECKING

import numpy as np

from dooders.sdk.base.base_policy import BasePolicy
from dooders.sdk.core.core import Core

if TYPE_CHECKING:
    from dooders.sdk.models.dooder import Dooder


def average(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
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
        The new Dooder weights

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


def random(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
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
        The new Dooder weights

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


def crossover(a_weights: np.ndarray, b_weights: np.ndarray) -> np.ndarray:
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
        The new Dooder weights

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
        The new Dooder weights

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


@Core.register('policy')
class AverageWeights(BasePolicy):
    """
    Taking the model weights from two Dooders and averaging them to use with a new Dooder.

    Averages the weights of two Dooders to create a new Dooder.

    Parameters
    ----------
    dooderA (Dooder): Dooder
        The first Dooder.
    dooderB (Dooder): Dooder
        The second Dooder.

    Returns
    -------
    new_weights : (np.ndarray)
        The new Dooder weights

    Methods
    -------
    execute(dooderA: Dooder, dooderB: Dooder) -> np.ndarray
        Averages the weights of two Dooders to create a new Dooder.
    """

    @classmethod
    def execute(cls, agentA: 'Dooder', agentB: 'Dooder') -> np.ndarray:
        """
        This method computes the average weights of two agents' internal models.

        Args:
            agentA: The first agent.
            agentB: The second agent.

        Returns:
            new_weights: A dictionary containing the average weights of the agents' internal models.
        """
        new_weights = {}
        weightsA = agentA.internal_models.weights
        weightsB = agentB.internal_models.weights

        model_names = list(weightsA.keys())

        for model in model_names:
            new_weights[model] = []
            a_weights = weightsA[model]
            b_weights = weightsB[model]

            combined_weights = []

            for i in range(len(a_weights)):
                combined_weights.append((a_weights[i] + b_weights[i]) / 2)

            new_weights[model] = combined_weights

        return new_weights


@Core.register('policy')
class RangeWeights(BasePolicy):
    """
    Taking the model weights from two Dooders and randomly selecting weights 
    between the range of the two Dooder to use with a new Dooder.

    Randomly selects weights between the range of the two Dooders to create a new Dooder.

    Parameters
    ----------
    dooderA : Dooder
        The first Dooder.
    dooderB : Dooder
        The second Dooder.

    Returns
    -------
    new_weights : (np.ndarray) 
        The new Dooder weights

    Methods
    -------
    execute(dooderA: Dooder, dooderB: Dooder) -> np.ndarray
        Randomly selects weights between the range of the two 
        Dooders to create a new Dooder.
    """

    @classmethod
    def execute(self, dooderA: 'Dooder', dooderB: 'Dooder') -> np.ndarray:
        new_weights = {}
        weightsA = dooderA.internal_models.weights
        weightsB = dooderB.internal_models.weights

        for key in weightsA.keys():
            modelA = weightsA[key]
            modelB = weightsB[key]

            new_weights[key] = {}

            for k in modelA.keys():
                mA = modelA[k]
                mB = modelB[k]
                new_weights[key][k] = [np.random.uniform(mA, mB)]

        return new_weights


@Core.register('policy')
class SplitWeights(BasePolicy):
    """
    Taking the model weights from two Dooders. The first layer weights of DooderA
    and the second layer weights from DooderB.
    Then use those weights in a new Dooder.

    Takes the first layer weights from DooderA and the second layer weights from DooderB.
    Then use those weights in a new Dooder.

    Parameters
    ----------
    dooderA : Dooder
        The first Dooder.
    dooderB : Dooder
        The second Dooder.

    Returns
    -------
    new_weights : (np.ndarray)
        The new Dooder weights

    Methods
    -------
    execute(dooderA: Dooder, dooderB: Dooder) -> np.ndarray
        Takes the first layer weights from DooderA and the 
        second layer weights from DooderB.
    """

    @classmethod
    def execute(self, dooderA: 'Dooder', dooderB: 'Dooder') -> np.ndarray:
        new_weights = {}
        weightsA = dooderA.internal_models.weights
        weightsB = dooderB.internal_models.weights

        for key in weightsA.keys():
            modelA = weightsA[key]
            modelB = weightsB[key]

            new_weights[key] = {}

            for k in modelA.keys():
                mA = modelA[k]
                mB = modelB[k]
                new_weights[key][k] = [mA[0], mB[1]]

        return new_weights
