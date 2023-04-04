from typing import List

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import InverseTimeDecay


class SimpleNeuralNet:
    """
    A simple neural network with 2 hidden layers

    Attributes
    ----------
    model : tf.keras.Sequential
        The model

    Methods
    -------
    predict(input_array: np.ndarray) -> int
        Predict the class of the input data
    """

    def __init__(self) -> None:
        """
        Initialize the model
        """
        initial_learning_rate = 0.001
        decay_rate = 5e-7
        lr_schedule = InverseTimeDecay(
            initial_learning_rate,
            decay_steps=1,
            decay_rate=decay_rate,
            staircase=False
        )

        self.model = Sequential([
            Dense(512, activation='relu', input_shape=(9,)),
            Dense(9, activation='softmax')
        ])

        self.model.compile(
            loss='categorical_crossentropy',
            optimizer=Adam(learning_rate=lr_schedule),
            metrics=['accuracy']
        )

    def predict(self, input_array: np.ndarray) -> int:
        """
        Predict the class of the input data

        Parameters
        ----------
        input_array : array
            The input data

        Returns
        -------
        int
            The class of the input data
        """
        self.input = input_array
        self.output = self.model(input_array.reshape(1, -1), training=True)
        prediction = np.argmax(self.output)

        return prediction

    def learn(self, reality: list) -> None:
        """
        Learn from the reality

        Parameters
        ----------
        reality : list
            The reality (truth)
        """
        self.reality = reality
        reality_array = np.array(self.reality, dtype='uint8')

        self.model.train_on_batch(self.input.reshape(
            1, -1), reality_array.reshape(1, -1))

    def inherit_weights(self, genetics: List[np.ndarray]) -> None:
        """
        Update the weights based on provided derived genetics
        from parent Dooders

        Parameters
        ----------
        genetics : List[np.ndarray]
            The weights of the neural network
        """
        self.model.layers[0].set_weights(genetics[0])
        self.model.layers[1].set_weights(genetics[1])

    def save(self, path: str) -> None:
        """
        Save the model

        Parameters
        ----------
        path : str
            The path to save the model
        """
        self.model.save(path)

    @property
    def layers(self) -> List[tf.keras.layers.Dense]:
        """ 
        Get the layers of the neural network
        
        Returns
        -------
        List[tf.keras.layers.Dense]
            The layers of the neural network
        """
        return self.model.layers

    @property
    def weights(self) -> List[np.ndarray]:
        """
        Get the weights of the neural network from every dense layer

        Returns
        -------
        np.ndarray
            The weights of the neural network
        """
        weights = [layer.get_weights() for layer in self.layers]
        return weights
