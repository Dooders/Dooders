from random import randrange, sample, randint
from typing import List
from pydantic import BaseModel


class Fate:

    def __init__():
        pass


def generate_probability():
    return randrange(100)


def generate_weights():
    return []


def generate_score():
    return randrange(100)


def generate_distribution(number_of_choices):
    """
    Generates a distribution of probabilities for a given number of choices.
    """
    #! TODO: apply different distributions
    dividers = sorted(sample(range(1, 100), number_of_choices - 1)) # random distribution
    return [a - b for a, b in zip(dividers + [100], [0] + dividers)]


def ask_fate(probability):
    if randint(1,100) < probability:
        return True
    else:
        return False


class Behavior(BaseModel):
    ActionSuccessProbability: int = generate_probability()
    TakeActionProbability: int = generate_probability()
    ActionSelectionWeights: List = generate_weights()
    MakeMoveProbability: int = generate_probability()
    MoveSuccessProbability: int = generate_probability()
    BreedSuccessProbability: int = generate_probability()
    BreedActionProbability: int = generate_probability()
    MoveDirectionDistribution: List = generate_distribution(9)
    AwarenessScore: int = generate_score()
    ActionOrderDistribution: List = generate_distribution(3)
    ActionPrivilegeScore: int = generate_score()
    HappinessScore: int = generate_score()
    EnvironmentScore: int = generate_score()


