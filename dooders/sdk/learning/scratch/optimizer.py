""" 
Code taken from "Neural Networks from Scratch" 
https://nnfs.io/
"""

import numpy as np

from dooders.sdk.learning.scratch import layer


class Optimizer_SGD:
    """ 
    Stochastic Gradient Descent optimizer

    Parameters
    ----------
    learning_rate : float, optional
        Learning rate, by default 1.
    decay : float, optional
        Decay rate, by default 0.
    momentum : float, optional
        Momentum, by default 0.

    Methods
    -------
    pre_update_params()
        Call once before any parameter updates
    update_params(layer)
        Update parameters
    post_update_params()
        Call once after any parameter updates

    Attributes
    ----------
    learning_rate : float
        Learning rate
    current_learning_rate : float
        Current learning rate
    decay : float
        Decay rate
    iterations : int
        Iterations
    momentum : float
        Momentum
    """

    def __init__(self,
                 learning_rate: float = 1.,
                 decay: float = 0.,
                 momentum: float = 0.) -> None:
        """ 
        Initialize optimizer - set settings,
        learning rate of 1. is default for this optimizer
        """
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.momentum = momentum

    def pre_update_params(self) -> None:
        """ 
        Call once before any parameter updates

        If decay is set,
        update the current learning rate
        """
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1. / (1. + self.decay * self.iterations))

    def update_params(self, layer: layer) -> None:
        """ 
        Update parameters

        Parameters
        ----------
        layer : Layer
            Layer to update
        """

        # If we use momentum
        if self.momentum:

            # If layer does not contain momentum arrays, create them
            # filled with zeros
            if not hasattr(layer, 'weight_momentums'):
                layer.weight_momentums = np.zeros_like(layer.weights)
                # If there is no momentum array for weights
                # The array doesn't exist for biases yet either.
                layer.bias_momentums = np.zeros_like(layer.biases)
            # Build weight updates with momentum - take previous
            # updates multiplied by retain factor and update with
            # current gradients
            weight_updates = \
                self.momentum * layer.weight_momentums - \
                self.current_learning_rate * layer.dweights
            layer.weight_momentums = weight_updates

            # Build bias updates
            bias_updates = \
                self.momentum * layer.bias_momentums - \
                self.current_learning_rate * layer.dbiases
            layer.bias_momentums = bias_updates

        # Vanilla SGD updates (as before momentum update)
        else:
            weight_updates = -self.current_learning_rate * \
                layer.dweights
            bias_updates = -self.current_learning_rate * \
                layer.dbiases

        # Update weights and biases using either
        # vanilla or momentum updates
        layer.weights += weight_updates
        layer.biases += bias_updates

    def post_update_params(self) -> None:
        """ 
        Call once after any parameter updates
        """
        self.iterations += 1


class Optimizer_Adagrad:
    """ 
    Adam grad optimizer

    Parameters
    ----------
    learning_rate : float, optional
        Learning rate, by default 1.
    decay : float, optional
        Decay rate, by default 0.
    epsilon : float, optional
        Small value to avoid division by zero, by default 1e-7

    Methods
    -------
    pre_update_params()
        Call once before any parameter updates
    update_params(layer)
        Update parameters
    post_update_params()
        Call once after any parameter updates

    Attributes
    ----------
    learning_rate : float
        Learning rate
    current_learning_rate : float
        Current learning rate
    decay : float
        Decay rate
    iterations : int
        Iterations
    epsilon : float
        Small value to avoid division by zero
    """

    def __init__(self,
                 learning_rate: float = 1.,
                 decay: float = 0.,
                 epsilon: float = 1e-7) -> None:
        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon

    def pre_update_params(self) -> None:
        """ 
        Call once before any parameter updates
        """
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1. / (1. + self.decay * self.iterations))

    def update_params(self, layer: layer) -> None:
        """ 
        Update parameters

        Parameters
        ----------
        layer : Layer
            Layer to update
        """
        # If layer does not contain cache arrays,
        # create them filled with zeros
        if not hasattr(layer, 'weight_cache'):
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_cache = np.zeros_like(layer.biases)

        # Update cache with squared current gradients
        layer.weight_cache += layer.dweights**2
        layer.bias_cache += layer.dbiases**2

        # Vanilla SGD parameter update + normalization
        # with square rooted cache
        layer.weights += -self.current_learning_rate * \
            layer.dweights / \
            (np.sqrt(layer.weight_cache) + self.epsilon)
        layer.biases += -self.current_learning_rate * \
            layer.dbiases / \
            (np.sqrt(layer.bias_cache) + self.epsilon)

    def post_update_params(self) -> None:
        """ 
        Call once after any parameter updates
        """
        self.iterations += 1


class Optimizer_RMSprop:
    """ 
    RMSprop optimizer

    Parameters
    ----------
    learning_rate : float, optional
        Learning rate, by default 0.001
    decay : float, optional
        Decay rate, by default 0.
    epsilon : float, optional
        Small value to avoid division by zero, by default 1e-7
    rho : float, optional
        Decay rate, by default 0.9

    Methods
    -------
    pre_update_params()
        Call once before any parameter updates
    update_params(layer)
        Update parameters
    post_update_params()
        Call once after any parameter updates

    Attributes
    ----------
    learning_rate : float
        Learning rate
    current_learning_rate : float
        Current learning rate
    decay : float
        Decay rate
    iterations : int
        Iterations
    epsilon : float
        Small value to avoid division by zero
    rho : float
        Decay rate
    """

    def __init__(self,
                 learning_rate: float = 0.001,
                 decay: float = 0.,
                 epsilon: float = 1e-7,
                 rho: float = 0.9) -> None:

        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon
        self.rho = rho

    def pre_update_params(self) -> None:
        """ 
        Call once before any parameter updates
        """
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1. / (1. + self.decay * self.iterations))

    def update_params(self, layer: layer) -> None:
        """ 
        Update parameters

        Parameters
        ----------
        layer : Layer
            Layer to update
        """

        # If layer does not contain cache arrays,
        # create them filled with zeros
        if not hasattr(layer, 'weight_cache'):
            layer.weight_cache = np.zeros_like(layer.weights)
            layer.bias_cache = np.zeros_like(layer.biases)

        # Update cache with squared current gradients
        layer.weight_cache = self.rho * layer.weight_cache + \
            (1 - self.rho) * layer.dweights**2
        layer.bias_cache = self.rho * layer.bias_cache + \
            (1 - self.rho) * layer.dbiases**2

        # Vanilla SGD parameter update + normalization
        # with square rooted cache
        layer.weights += -self.current_learning_rate * \
            layer.dweights / \
            (np.sqrt(layer.weight_cache) + self.epsilon)
        layer.biases += -self.current_learning_rate * \
            layer.dbiases / \
            (np.sqrt(layer.bias_cache) + self.epsilon)

    def post_update_params(self) -> None:
        """ 
        Call once after any parameter updates
        """
        self.iterations += 1

class Optimizer_Adam:
    __slots__ = ('learning_rate', 'current_learning_rate', 'decay', 'iterations', 'epsilon', 'beta_1', 'beta_2', 'cache')

    def __init__(self,
                 learning_rate: float = 0.001,
                 decay: float = 0.,
                 epsilon: float = 1e-7,
                 beta_1: float = 0.9,
                 beta_2: float = 0.999):

        self.learning_rate = learning_rate
        self.current_learning_rate = learning_rate
        self.decay = decay
        self.iterations = 0
        self.epsilon = epsilon
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.cache = {}

    def pre_update_params(self) -> None:
        if self.decay:
            self.current_learning_rate = self.learning_rate * \
                (1. / (1. + self.decay * self.iterations))

    def update_params(self, layer: layer) -> None:
        if layer not in self.cache:
            self.cache[layer] = {
                'weight_momentums': np.zeros_like(layer.weights),
                'weight_cache': np.zeros_like(layer.weights),
                'bias_momentums': np.zeros_like(layer.biases),
                'bias_cache': np.zeros_like(layer.biases)
            }

        cache = self.cache[layer]

        cache['weight_momentums'] = self.beta_1 * cache['weight_momentums'] + (1 - self.beta_1) * layer.dweights
        cache['bias_momentums'] = self.beta_1 * cache['bias_momentums'] + (1 - self.beta_1) * layer.dbiases

        weight_momentums_corrected = cache['weight_momentums'] / (1 - self.beta_1 ** (self.iterations + 1))
        bias_momentums_corrected = cache['bias_momentums'] / (1 - self.beta_1 ** (self.iterations + 1))

        cache['weight_cache'] = self.beta_2 * cache['weight_cache'] + (1 - self.beta_2) * layer.dweights**2
        cache['bias_cache'] = self.beta_2 * cache['bias_cache'] + (1 - self.beta_2) * layer.dbiases**2

        weight_cache_corrected = cache['weight_cache'] / (1 - self.beta_2 ** (self.iterations + 1))
        bias_cache_corrected = cache['bias_cache'] / (1 - self.beta_2 ** (self.iterations + 1))

        layer.weights -= self.current_learning_rate * weight_momentums_corrected / (np.sqrt(weight_cache_corrected) + self.epsilon)
        layer.biases -= self.current_learning_rate * bias_momentums_corrected / (np.sqrt(bias_cache_corrected) + self.epsilon)

    def post_update_params(self) -> None:
        self.iterations += 1
