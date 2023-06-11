"""
Functions for initializing weights
"""

import numpy as np


def initialize_weights(n_inputs: int, n_neurons: int, weight_init: str = 'random') -> np.ndarray:
    """ 
    Initializes weights using the specified method.
    
    Parameters
    ----------
    n_inputs : int
        Number of inputs.
    n_neurons : int
        Number of neurons.
    weight_init : str
        Weight initialization method.
    
    Returns
    -------
    weights : 2darray
        Randomly initialized weights.
    """
    
    if weight_init == 'random':
        return random_weights(n_inputs, n_neurons)
    elif weight_init == 'he':
        return he_weights(n_inputs, n_neurons)
    elif weight_init == 'xavier':
        return xavier_weights(n_inputs, n_neurons)
    else:
        raise ValueError(f'Unknown weight initialization method: {weight_init}')


def random_weights(n_inputs: int, n_neurons: int) -> np.ndarray:
    """ 
    Initializes weights randomly.
    
    Parameters
    ----------
    n_inputs : int
        Number of inputs.
    n_neurons : int
        Number of neurons.
    
    Returns
    -------
    weights : 2darray
        Randomly initialized weights.
    """
    
    return 0.01 * np.random.randn(n_inputs, n_neurons)


def he_weights(n_inputs: int, n_neurons: int) -> np.ndarray:
    """ 
    Initializes weights using He et al. initialization.
    
    Parameters
    ----------
    n_inputs : int
        Number of inputs.
    n_neurons : int
        Number of neurons.
    
    Returns
    -------
    weights : 2darray
        Randomly initialized weights.
    """
    
    return np.random.randn(n_inputs, n_neurons) * np.sqrt(2 / n_inputs)


def xavier_weights(n_inputs: int, n_neurons: int) -> np.ndarray:
    """ 
    Initializes weights using Xavier initialization.
    
    Parameters
    ----------
    n_inputs : int
        Number of inputs.
    n_neurons : int
        Number of neurons.

    Returns
    -------
    weights : 2darray
        Randomly initialized weights.
    """
    return np.random.randn(n_inputs, n_neurons) * np.sqrt(1 / n_inputs)