""" 
Code taken from "Neural Networks from Scratch" 
https://nnfs.io/
"""

import numpy as np

from dooders.sdk.learning.scratch.weights import initialize_weights


class Layer_Dense:
    """ 
    A dense layer is just a layer which performs a dot product
    between input and weights, and then adds biases.

    It also holds the weights and biases, as well as the
    derivatives of the weights and biases with respect to the
    loss function.

    Parameters
    ----------
    n_inputs : int
        Number of inputs coming into the layer.
    n_neurons : int
        Number of neurons in the layer.
    weight_regularizer_l1 : float
        L1 regularization strength. Defaults to 0.
    weight_regularizer_l2 : float
        L2 regularization strength. Defaults to 0.
    bias_regularizer_l1 : float
        L1 regularization strength. Defaults to 0.
    bias_regularizer_l2 : float
        L2 regularization strength. Defaults to 0.

    Attributes
    ----------
    weights : 2darray
        Weights of the layer.
    biases : 2darray
        Biases of the layer.
    weight_regularizer_l1 : float
        L1 regularization strength.
    weight_regularizer_l2 : float
        L2 regularization strength.
    bias_regularizer_l1 : float
        L1 regularization strength.
    bias_regularizer_l2 : float
        L2 regularization strength.
    dweights : 2darray
        Derivative of the weights with respect to the loss function.
    dbiases : 2darray
        Derivative of the biases with respect to the loss function.
    dinputs : 2darray
        Derivative of the inputs with respect to the loss function.
    inputs : 2darray
        Inputs to the layer.
    output : 2darray
        Output of the layer.

    Methods
    -------
    forward(inputs, training)
        Performs a forward pass of the layer.
    backward(dvalues)
        Performs a backward pass of the layer.
    """

    def __init__(self, n_inputs, n_neurons,
                 weight_regularizer_l1=0, weight_regularizer_l2=0,
                 bias_regularizer_l1=0, bias_regularizer_l2=0,
                 frozen=False) -> None:
        # Initialize weights and biases
        self.weights = initialize_weights(
            n_inputs, n_neurons, weight_init='random')
        self.biases = np.zeros((1, n_neurons))
        self.frozen = frozen
        # Set regularization strength
        self.weight_regularizer_l1 = weight_regularizer_l1
        self.weight_regularizer_l2 = weight_regularizer_l2
        self.bias_regularizer_l1 = bias_regularizer_l1
        self.bias_regularizer_l2 = bias_regularizer_l2

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Performs a forward pass of the layer.

        Parameters
        ----------
        inputs : 2darray
            Inputs to the layer.
        training : bool
            Whether or not the layer is in training mode.
        """
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs, weights and biases
        self.output = np.dot(inputs, self.weights) + self.biases

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Performs a backward pass of the layer.

        Parameters
        ----------
        dvalues : 2darray
            Derivative of the loss function with respect to the layer's output.
        """

        # Gradients on parameters
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)

        # Gradients on regularization
        # L1 on weights
        if self.weight_regularizer_l1 > 0:
            dL1 = np.ones_like(self.weights)
            dL1[self.weights < 0] = -1
            self.dweights += self.weight_regularizer_l1 * dL1
        # L2 on weights
        if self.weight_regularizer_l2 > 0:
            self.dweights += 2 * self.weight_regularizer_l2 * \
                self.weights
        # L1 on biases
        if self.bias_regularizer_l1 > 0:
            dL1 = np.ones_like(self.biases)
            dL1[self.biases < 0] = -1
            self.dbiases += self.bias_regularizer_l1 * dL1
        # L2 on biases
        if self.bias_regularizer_l2 > 0:
            self.dbiases += 2 * self.bias_regularizer_l2 * \
                self.biases

        # Gradient on values
        self.dinputs = np.dot(dvalues, self.weights.T)


class Layer_Dropout:
    """ 
    Dropout layer randomly sets a fraction of input values to zero.

    Parameters
    ----------
    rate : float
        Fraction of the input values to be set to zero.

    Attributes
    ----------
    rate : float
        Fraction of the input values to be set to zero.
    binary_mask : 2darray
        Binary mask used to set values to zero.
    inputs : 2darray
        Inputs to the layer.
    output : 2darray
        Output of the layer.

    Methods
    -------
    forward(inputs, training)
        Performs a forward pass of the layer.
    backward(dvalues)
        Performs a backward pass of the layer.
    """

    def __init__(self, rate: float) -> None:
        # Store rate, we invert it as for example for dropout
        # of 0.1 we need success rate of 0.9
        self.rate = 1 - rate

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Performs a forward pass of the layer.

        Parameters
        ----------
        inputs : 2darray
            Inputs to the layer.
        training : bool
            Whether or not the layer is in training mode.
        """
        # Save input values
        self.inputs = inputs

        # If not in the training mode - return values
        if not training:
            self.output = inputs.copy()
            return

        # Generate and save scaled mask
        self.binary_mask = np.random.binomial(1, self.rate,
                                              size=inputs.shape) / self.rate
        # Apply mask to output values
        self.output = inputs * self.binary_mask

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Performs a backward pass of the layer.

        Parameters
        ----------
        dvalues : 2darray
            Derivative of the loss function with respect to the layer's output.
        """
        # Gradient on values
        self.dinputs = dvalues * self.binary_mask


class Layer_Input:
    """ 
    Input layer of a neural network.

    Parameters
    ----------
    n_inputs : int
        Number of inputs to the layer.

    Attributes
    ----------
    n_inputs : int
        Number of inputs to the layer.
    output : 2darray
        Output of the layer.

    Methods
    -------
    forward(inputs, training)
        Performs a forward pass of the layer.
    backward(dvalues)
        Performs a backward pass of the layer.
    """

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Performs a forward pass of the layer.

        Parameters
        ----------
        inputs : 2darray
            Inputs to the layer.
        training : bool
            Whether or not the layer is in training mode.
        """
        self.output = inputs
