""" 
Code taken from "Neural Networks from Scratch" 
https://nnfs.io/
"""

import numpy as np


class Loss:
    """ 
    Loss base class

    Methods
    -------
    regularization_loss(self) -> float
        Calculates the regularization loss
    remember_trainable_layers(self, trainable_layers)
        Remembers the trainable layers
    calculate(self, output, y, *, include_regularization=False)
        Calculates the data and regularization losses
        given model output and ground truth values

    Attributes
    ----------
    dinputs
        Gradient of the loss function
    """

    def regularization_loss(self) -> float:
        """ 
        Calculates the regularization loss

        Returns
        -------
        float
            Regularization loss
        """

        # 0 by default
        regularization_loss = 0

        # Calculate regularization loss
        # iterate all trainable layers
        for layer in self.trainable_layers:

            # L1 regularization - weights
            # calculate only when factor greater than 0
            if layer.weight_regularizer_l1 > 0:
                regularization_loss += layer.weight_regularizer_l1 * \
                    np.sum(np.abs(layer.weights))

            # L2 regularization - weights
            if layer.weight_regularizer_l2 > 0:
                regularization_loss += layer.weight_regularizer_l2 * \
                    np.sum(layer.weights *
                           layer.weights)

            # L1 regularization - biases
            # calculate only when factor greater than 0
            if layer.bias_regularizer_l1 > 0:
                regularization_loss += layer.bias_regularizer_l1 * \
                    np.sum(np.abs(layer.biases))

            # L2 regularization - biases
            if layer.bias_regularizer_l2 > 0:
                regularization_loss += layer.bias_regularizer_l2 * \
                    np.sum(layer.biases *
                           layer.biases)

        return regularization_loss

    def remember_trainable_layers(self, trainable_layers: list) -> None:
        """ 
        Remembers the trainable layers

        Parameters
        ----------
        trainable_layers : list
            List of trainable layers
        """
        self.trainable_layers = trainable_layers

    def calculate(self,
                  output: np.ndarray,
                  y: np.ndarray,
                  *,
                  include_regularization: bool = False) -> float:
        """ 
        Calculates the data and regularization losses
        given model output and ground truth values

        Parameters
        ----------
        output : np.ndarray
            Model output
        y : np.ndarray
            Ground truth values
        include_regularization : bool, optional
            Whether to include regularization loss, by default False
        """
        # Calculate sample losses
        sample_losses = self.forward(output, y)

        # Calculate mean loss
        data_loss = np.mean(sample_losses)

        # If just data loss - return it
        if not include_regularization:
            return data_loss

        # Return the data and regularization losses
        return data_loss, self.regularization_loss()


class Loss_CategoricalCrossentropy(Loss):
    """ 
    Categorical cross-entropy loss

    Methods
    -------
    forward(self, y_pred, y_true)
        Calculates the forward pass
    backward(self, dvalues, y_true)
        Calculates the backward pass

    Attributes
    ----------
    dinputs
        Gradient of the loss function
    """

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """ 
        Calculates the forward pass

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            Ground truth values

        Returns
        -------
        np.ndarray
            Loss
        """
        # Number of samples in a batch
        samples = len(y_pred)

        # Clip data to prevent division by 0
        # Clip both sides to not drag mean towards any value
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

        # Probabilities for target values -
        # only if categorical labels
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[
                range(samples),
                y_true
            ]

        # Mask values - only for one-hot encoded labels
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(
                y_pred_clipped * y_true,
                axis=1
            )

        # Losses
        negative_log_likelihoods = -np.log(correct_confidences)
        return negative_log_likelihoods

    def backward(self, dvalues: np.ndarray, y_true: np.ndarray) -> None:
        """ 
        Calculates the backward pass

        Parameters
        ----------
        dvalues : np.ndarray
            Gradient of the loss function
        y_true : np.ndarray
            Ground truth values
        """
        samples = len(dvalues)
        # Number of labels in every sample
        # We'll use the first sample to count them
        labels = len(dvalues[0])

        # If labels are sparse, turn them into one-hot vector
        if len(y_true.shape) == 1:
            y_true = np.eye(labels)[y_true]

        # Calculate gradient
        self.dinputs = -y_true / dvalues
        # Normalize gradient
        self.dinputs = self.dinputs / samples


class Activation_Softmax_Loss_CategoricalCrossentropy(Loss):
    """ 
    Softmax classifier - combined Softmax activation
    and cross-entropy loss for faster backward step

    Methods
    -------
    backward(self, dvalues, y_true)
        Calculates the backward pass

    Attributes
    ----------
    activation
        Softmax activation
    loss
        Categorical cross-entropy loss
    dinputs
        Gradient of the loss function
    """

    def backward(self, dvalues: np.ndarray, y_true: np.ndarray) -> None:
        """ 
        Calculates the backward pass

        Parameters
        ----------
        dvalues : np.ndarray
            Gradient of the loss function
        y_true : np.ndarray
            Ground truth values
        """

        # Number of samples
        samples = len(dvalues)

        # If labels are one-hot encoded,
        # turn them into discrete values
        if len(y_true.shape) == 2:
            y_true = np.argmax(y_true, axis=1)

        # Copy so we can safely modify
        self.dinputs = dvalues.copy()
        # Calculate gradient
        self.dinputs[range(samples), y_true] -= 1
        # Normalize gradient
        self.dinputs = self.dinputs / samples


class Loss_BinaryCrossentropy(Loss):
    """ 
    Binary cross-entropy loss

    Methods
    -------
    forward(self, y_pred, y_true)
        Calculates the forward pass
    backward(self, dvalues, y_true)
        Calculates the backward pass

    Attributes
    ----------
    dinputs
        Gradient of the loss function
    """

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """ 
        Calculates the forward pass

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            Ground truth values

        Returns
        -------
        np.ndarray
            Loss
        """
        # Clip data to prevent division by 0
        # Clip both sides to not drag mean towards any value
        y_pred_clipped = np.clip(y_pred, 1e-7, 1 - 1e-7)

        # Calculate sample-wise loss
        sample_losses = -(y_true * np.log(y_pred_clipped) +
                          (1 - y_true) * np.log(1 - y_pred_clipped))
        sample_losses = np.mean(sample_losses, axis=-1)

        # Return losses
        return sample_losses

    def backward(self, dvalues: np.ndarray, y_true: np.ndarray) -> None:
        """ 
        Calculates the backward pass

        Parameters
        ----------
        dvalues : np.ndarray
            Gradient of the loss function
        y_true : np.ndarray
            Ground truth values
        """

        if len(y_true) > 1:
            for y in y_true:
                samples = len(dvalues)
                # Number of outputs in every sample
                # We'll use the first sample to count them
                outputs = len(dvalues[0])

                # Clip data to prevent division by 0
                # Clip both sides to not drag mean towards any value
                clipped_dvalues = np.clip(dvalues, 1e-7, 1 - 1e-7)

                # Calculate gradient
                self.dinputs = -(y / clipped_dvalues -
                                 (1 - y) / (1 - clipped_dvalues)) / outputs
                # Normalize gradient
                self.dinputs = self.dinputs / samples
        else:

            # Number of samples
            samples = len(dvalues)
            # Number of outputs in every sample
            # We'll use the first sample to count them
            outputs = len(dvalues[0])

            # Clip data to prevent division by 0
            # Clip both sides to not drag mean towards any value
            clipped_dvalues = np.clip(dvalues, 1e-7, 1 - 1e-7)

            # Calculate gradient
            self.dinputs = -(y_true / clipped_dvalues -
                             (1 - y_true) / (1 - clipped_dvalues)) / outputs
            # Normalize gradient
            self.dinputs = self.dinputs / samples


class Loss_MeanSquaredError(Loss):
    """ 
    L2 loss (mean squared error)

    Methods
    -------
    forward(self, y_pred, y_true)
        Calculates the forward pass
    backward(self, dvalues, y_true)
        Calculates the backward pass

    Attributes
    ----------
    dinputs
        Gradient of the loss function
    """

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """ 
        Calculates the forward pass

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            Ground truth values

        Returns
        -------
        np.ndarray
            Loss
        """

        # Calculate loss
        sample_losses = np.mean((y_true - y_pred)**2, axis=-1)

        # Return losses
        return sample_losses

    def backward(self, dvalues: np.ndarray, y_true: np.ndarray) -> None:
        """ 
        Calculates the backward pass

        Parameters
        ----------
        dvalues : np.ndarray
            Gradient of the loss function
        y_true : np.ndarray
            Ground truth values
        """

        # Number of samples
        samples = len(dvalues)
        # Number of outputs in every sample
        # We'll use the first sample to count them
        outputs = len(dvalues[0])

        # Gradient on values
        self.dinputs = -2 * (y_true - dvalues) / outputs
        # Normalize gradient
        self.dinputs = self.dinputs / samples


class Loss_MeanAbsoluteError(Loss):
    """ 
    L1 loss (mean absolute error)

    Methods
    -------
    forward(self, y_pred, y_true)
        Calculates the forward pass
    backward(self, dvalues, y_true)
        Calculates the backward pass

    Attributes
    ----------
    dinputs
        Gradient of the loss function
    """

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> np.ndarray:
        """ 
        Calculates the forward pass

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            Ground truth values

        Returns
        -------
        np.ndarray
            Loss
        """

        # Calculate loss
        sample_losses = np.mean(np.abs(y_true - y_pred), axis=-1)

        # Return losses
        return sample_losses

    def backward(self, dvalues: np.ndarray, y_true: np.ndarray) -> None:
        """ 
        Calculates the backward pass

        Parameters
        ----------
        dvalues : np.ndarray
            Gradient of the loss function
        y_true : np.ndarray
            Ground truth values
        """

        # Number of samples
        samples = len(dvalues)
        # Number of outputs in every sample
        # We'll use the first sample to count them
        outputs = len(dvalues[0])

        # Calculate gradient
        self.dinputs = np.sign(y_true - dvalues) / outputs
        # Normalize gradient
        self.dinputs = self.dinputs / samples


class MultiLabelBinaryCrossEntropy(Loss):
    def __init__(self):
        self.loss = None
        self.epsilon = 1e-15

    def forward(self, y_pred: np.ndarray, y_true: np.ndarray) -> None:
        """ 
        Calculates the forward pass

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            Ground truth values
        """
        self.loss = -np.sum(y_true * np.log(y_pred) +
                            (1 - y_true) * np.log(1 - y_pred))

    def backward(self, y_pred: np.ndarray, y_true: np.ndarray) -> None:
        """
        Calculates the backward pass

        Parameters
        ----------
        y_pred : np.ndarray
            Predicted values
        y_true : np.ndarray
            Ground truth values
        """

        #! Do this part earlier
        test_elements = np.arange(0, 9)
        result = np.isin(test_elements, y_true)
        #!

        y_pred_clipped = np.clip(result, self.epsilon, 1 - self.epsilon)

        self.forward(y_pred_clipped, result)

        samples = y_pred.shape[0]

        # Calculate the gradient
        self.dinputs = -(result / y_pred_clipped -
                         (1 - result) / (1 - y_pred_clipped))

        # Normalize the gradient
        self.dinputs = self.dinputs / samples


LOSS = {
    'binary_crossentropy': Loss_BinaryCrossentropy,
    'categorical_crossentropy': Activation_Softmax_Loss_CategoricalCrossentropy,
    'mean_squared_error': Loss_MeanSquaredError,
    'mean_absolute_error': Loss_MeanAbsoluteError,
    'multilabel_binary_crossentropy': MultiLabelBinaryCrossEntropy,
}
