""" 
Code taken from "Neural Networks from Scratch" 
https://nnfs.io/
"""

import numpy as np


# ReLU activation
class Activation_ReLU:
    """ 
    ReLU activation

    Methods
    -------
    forward(inputs, training)
        Forward pass
    backward(dvalues)
        Backward pass
    predictions(outputs)
        Calculate predictions for outputs

    Attributes
    ----------
    inputs : array
        Input values
    output : array
        Output values
    dinputs : array
        Input gradients
    """

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Forward pass

        Parameters
        ----------
        inputs : array
            Input values
        training : bool
            True if training, False if testing
        """
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs
        self.output = np.maximum(0, inputs)

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Backward pass

        Parameters
        ----------
        dvalues : array
            Gradient of loss function
        """
        # Since we need to modify original variable,
        # let's make a copy of values first
        self.dinputs = dvalues.copy()

        # Zero gradient where input values were negative
        self.dinputs[self.inputs <= 0] = 0

    def predictions(self, outputs: np.ndarray) -> np.ndarray:
        """ 
        Calculate predictions for outputs

        Parameters
        ----------
        outputs : array
            Output values

        Returns
        -------
        array
            Predictions
        """
        return outputs


class Activation_Softmax:
    """ 
    Softmax activation

    Methods
    -------
    forward(inputs, training)
        Forward pass
    backward(dvalues)
        Backward pass
    predictions(outputs)
        Calculate predictions for outputs

    Attributes
    ----------
    inputs : array
        Input values
    output : array
        Output values
    dinputs : array
        Input gradients
    """

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Forward pass

        Parameters
        ----------
        inputs : array
            Input values
        training : bool
            True if training, False if testing
        """
        # Remember input values
        self.inputs = inputs

        # Get unnormalized probabilities
        exp_values = np.exp(inputs - np.max(inputs, axis=1,
                                            keepdims=True))

        # Normalize them for each sample
        probabilities = exp_values / np.sum(exp_values, axis=1,
                                            keepdims=True)

        self.output = probabilities

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Backward pass

        Parameters
        ----------
        dvalues : array
            Gradient of loss function
        """
        # Create uninitialized array
        self.dinputs = np.empty_like(dvalues)

        # Enumerate outputs and gradients
        for index, (single_output, single_dvalues) in \
                enumerate(zip(self.output, dvalues)):
            # Flatten output array
            single_output = single_output.reshape(-1, 1)
            # Calculate Jacobian matrix of the output
            jacobian_matrix = np.diagflat(single_output) - \
                np.dot(single_output, single_output.T)
            # Calculate sample-wise gradient
            # and add it to the array of sample gradients
            self.dinputs[index] = np.dot(jacobian_matrix,
                                         single_dvalues)

    def predictions(self, outputs: np.ndarray) -> np.ndarray:
        """ 
        Calculate predictions for outputs

        Parameters
        ----------
        outputs : array
            Output values

        Returns
        -------
        array
            Predictions
        """
        return np.argmax(outputs, axis=1)


class Activation_Sigmoid:
    """ 
    Sigmoid activation

    Methods
    -------
    forward(inputs, training)
        Forward pass
    backward(dvalues)
        Backward pass
    predictions(outputs)
        Calculate predictions for outputs

    Attributes
    ----------
    inputs : array
        Input values
    output : array
        Output values
    dinputs : array
        Input gradients
    """

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Forward pass

        Parameters
        ----------
        inputs : array
            Input values
        training : bool
            True if training, False if testing
        """
        # Save input and calculate/save output
        # of the sigmoid function
        self.inputs = inputs
        self.output = 1 / (1 + np.exp(-inputs))

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Backward pass

        Parameters
        ----------
        dvalues : array
            Gradient of loss function
        """
        # Derivative - calculates from output of the sigmoid function
        self.dinputs = dvalues * (1 - self.output) * self.output

    def predictions(self, outputs: np.ndarray) -> np.ndarray:
        """ 
        Calculate predictions for outputs

        Parameters
        ----------
        outputs : array
            Output values

        Returns
        -------
        array
            Predictions
        """
        return (outputs > 0.5) * 1


class Activation_Linear:
    """ 
    Linear activation

    Methods
    -------
    forward(inputs, training)
        Forward pass
    backward(dvalues)
        Backward pass
    predictions(outputs)
        Calculate predictions for outputs

    Attributes
    ----------
    inputs : array
        Input values
    output : array
        Output values
    dinputs : array
        Input gradients
    """

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Forward pass

        Parameters
        ----------
        inputs : array
            Input values
        training : bool
            True if training, False if testing
        """
        # Just remember values
        self.inputs = inputs
        self.output = inputs

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Backward pass

        Parameters
        ----------
        dvalues : array
            Gradient of loss function
        """
        # derivative is 1, 1 * dvalues = dvalues - the chain rule
        self.dinputs = dvalues.copy()

    def predictions(self, outputs: np.ndarray) -> np.ndarray:
        """ 
        Calculate predictions for outputs

        Parameters
        ----------
        outputs : array
            Output values

        Returns
        -------
        array
            Predictions
        """
        return outputs


class Activation_LeakyReLU:
    """ 
    Leaky ReLU activation

    Methods
    -------
    forward(inputs, training)
        Forward pass
    backward(dvalues)
        Backward pass
    predictions(outputs)
        Calculate predictions for outputs

    Attributes
    ----------
    inputs : array
        Input values
    output : array
        Output values
    dinputs : array
        Input gradients
    """

    def __init__(self, alpha: float = 0.01) -> None:
        self.alpha = alpha

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """ 
        Forward pass

        Parameters
        ----------
        inputs : array
            Input values
        training : bool
            True if training, False if testing
        """
        # Remember input values
        self.inputs = inputs
        # Calculate output values from inputs
        self.output = np.maximum(self.alpha * inputs, inputs)

    def backward(self, dvalues: np.ndarray) -> None:
        """ 
        Backward pass

        Parameters
        ----------
        dvalues : array
            Gradient of loss function
        """
        # Since we need to modify the original variable,
        # let's make a copy of values first
        self.dinputs = dvalues.copy()

        # Zero gradient where input values were negative
        self.dinputs[self.inputs <= 0] = self.alpha

    def predictions(self, outputs: np.ndarray) -> np.ndarray:
        """ 
        Calculate predictions for outputs

        Parameters
        ----------
        outputs : array
            Output values

        Returns
        -------
        array
            Predictions
        """
        return outputs


class Activation_ELU:
    """
    ELU activation

    Methods
    -------
    forward(inputs, training)
        Forward pass
    backward(dvalues)
        Backward pass
    predictions(outputs)
        Calculate predictions for outputs

    Attributes
    ----------
    inputs : array
        Input values
    output : array
        Output values
    dinputs : array
        Input gradients
    alpha : float
        ELU activation parameter
    """

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def forward(self, inputs: np.ndarray, training: bool) -> None:
        """
        Forward pass

        Parameters
        ----------
        inputs : array
            Input values
        training : bool
            True if training, False if testing
        """
        # Remember input values
        self.inputs = inputs

        # Calculate output values from inputs
        self.output = np.where(
            inputs > 0, inputs, self.alpha * (np.exp(inputs) - 1))

    def backward(self, dvalues: np.ndarray) -> None:
        """
        Backward pass

        Parameters
        ----------
        dvalues : array
            Gradient of loss function
        """
        # Since we need to modify the original variable,
        # let's make a copy of values first
        self.dinputs = dvalues.copy()

        # Calculate gradient
        self.dinputs[self.inputs <= 0] = self.dinputs[self.inputs <=
                                                      0] * (self.alpha * np.exp(self.inputs[self.inputs <= 0]))

    def predictions(self, outputs: np.ndarray) -> np.ndarray:
        """
        Calculate predictions for outputs

        Parameters
        ----------
        outputs : array
            Output values

        Returns
        -------
        array
            Predictions
        """
        return outputs


ACTIVATIONS = {
    "relu": Activation_ReLU,
    "softmax": Activation_Softmax,
    "sigmoid": Activation_Sigmoid,
    "linear": Activation_Linear,
    "leaky_relu": Activation_LeakyReLU,
    "elu": Activation_ELU,
}
