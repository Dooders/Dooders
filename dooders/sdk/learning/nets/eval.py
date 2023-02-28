""" 
Code taken from "Neural Networks from Scratch" 
https://nnfs.io/
"""

import numpy as np


class Accuracy:
    """ 
    Base class for accuracy calculation

    Methods
    -------
    calculate(predictions, y)
        Calculates an accuracy
    """

    def calculate(self, predictions: np.ndarray, y: np.ndarray) -> float:
        """ 
        Calculates an accuracy

        Parameters
        ----------
        predictions : np.ndarray
            Predictions from the model
        y : np.ndarray
            Ground truth values

        Returns
        -------
        float
            Accuracy
        """

        # Get comparison results
        comparisons = self.compare(predictions, y)

        # Calculate an accuracy
        accuracy = np.mean(comparisons)

        # Return accuracy
        return accuracy


class Accuracy_Categorical(Accuracy):
    """ 
    Accuracy calculation for classification model

    Parameters
    ----------
    binary : bool, optional
    """

    def __init__(self, *, binary=False) -> None:
        # Binary mode?
        self.binary = binary

    def init(self, y):
        pass

    def compare(self, predictions: np.ndarray, y: np.ndarray) -> np.ndarray:
        """ 
        Compares predictions to the ground truth values

        Parameters
        ----------
        predictions : np.ndarray
            Predictions from the model
        y : np.ndarray
            Ground truth values

        Returns
        -------
        np.ndarray
            Comparison results
        """
        if not self.binary and len(y.shape) == 2:
            y = np.argmax(y, axis=1)
        return predictions == y


# Accuracy calculation for regression model
class Accuracy_Regression(Accuracy):
    """ 
    Accuracy calculation for regression model
    """

    def __init__(self) -> None:
        # Create precision property
        self.precision = None

    def init(self, y: np.ndarray, reinit=False) -> None:
        """ 
        Initializes the precision property

        Parameters
        ----------
        y : np.ndarray
            Ground truth values
        reinit : bool, optional
            Reinitialize the precision property
        """
        if self.precision is None or reinit:
            self.precision = np.std(y) / 250

    def compare(self, predictions: np.ndarray, y: np.ndarray) -> np.ndarray:
        """ 
        Compares predictions to the ground truth values

        Parameters
        ----------
        predictions : np.ndarray
            Predictions from the model
        y : np.ndarray
            Ground truth values

        Returns
        -------
        np.ndarray
            Comparison results
        """
        return np.absolute(predictions - y) < self.precision
