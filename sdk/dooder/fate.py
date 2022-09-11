from random import randint, randrange, sample
from typing import List


class Fate:
    """ 
    Fate class used to decide the "fate" of an action.
    """

    @classmethod
    def generate_probability(cls) -> int:
        """  
        Generate a random probability

        Returns:
            int: A random probability between 0 and 100
        """
        # add different distros and options
        return randrange(1, 100)

    @classmethod
    def generate_weights(cls) -> List[int]:
        """ 
        Generate a list of random weights

        TBD
        """

        return [None]

    @classmethod
    def generate_score(cls) -> int:
        """ 
        Generate a random score

        Returns:
            int: A random score between 0 and 100
        """

        return randrange(1, 100)

    @classmethod
    def generate_distribution(cls, number_of_choices: int) -> List[int]:
        """
        Generates a distribution of probabilities for a given number of choices.

        Args:
            number_of_choices: The number of choices to generate probabilities for.

        Returns:
            List[int]: A list of probabilities for the given number of choices. Adding up to 100.
        """

        #! TODO: apply different distributions
        dividers = sorted(sample(range(1, 100), number_of_choices - 1))
        return [a - b for a, b in zip(dividers + [100], [0] + dividers)]

    @classmethod
    def ask_fate(cls, probability: int) -> bool:
        """ 
        Ask fate if the action is successful

        Args:
            probability: The probability of the action being successful.

        Returns:
            bool: True if the action is successful, False otherwise.
        """

        if randint(1, 100) < probability:
            return True
        else:
            return False
