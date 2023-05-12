from random import randrange

import numpy as np


class Scenario:
    """ 
    Scenario class is responsible for creating input data
    for Dooder internal models based on defined scenario methods

    Methods
    -------
    random(n: int = 9) -> np.ndarray
        Create a random input array for Dooder internal models
    run(type: str = 'random') -> np.ndarray
        Run a scenario method and return the output
    """

    results: list = []

    @classmethod
    def random(cls, n: int = 9) -> np.ndarray:
        """ 
        Create a random input array for Dooder internal models

        Parameters
        ----------
        n : int
            The size of the input array

        Returns
        -------
        np.ndarray
            The input array
        """
        base_array = np.zeros(n, dtype='uint8')
        position = randrange(n)
        base_array[position] = 1

        return position, base_array

    @classmethod
    def generate_input(cls, type: str = 'random') -> np.ndarray:
        """ 
        Run a scenario method and return the output

        Parameters
        ----------
        type : str
            The name of the scenario method to run

        Returns
        -------
        np.ndarray
            The output of the scenario method
        """
        method = getattr(cls, type)
        return method()

    @classmethod
    def _run(cls, model) -> None:
        """ 
        Run a scenario method and return the output

        Parameters
        ----------
        model : object
            The model to test
        """

        position, input_array = cls.generate_input()
        result = model.predict(input_array)

        if result == position:
            cls.results.append(1)
        else:
            cls.results.append(0)

    @classmethod
    def run(cls, model, runs: int = 10000) -> list:
        """ 
        Run a scenario method and return the output

        Parameters
        ----------
        model : object
            The model to test
        runs : int
            The number of times to run the scenario method

        Returns
        -------
        list
            The results of the scenario run
        """

        for _ in range(runs):
            cls._run(model)

        return cls.accuracy, cls.results

    @classmethod
    @property
    def accuracy(cls) -> float:
        """ 
        Calculate the accuracy of the scenario run

        Returns
        -------
        float
            The accuracy of the scenario run
        """

        return sum(cls.results) / len(cls.results)
