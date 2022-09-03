from random import randint, randrange, sample
from typing import Any, List

from pydantic import BaseModel, Field


class Fate:

    def __init__():
        pass


def generate_probability():
    """  """
    return randrange(100)


def generate_weights():
    return [None]


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
    ActionSuccessProbability: int = Field(default_factory=generate_probability)
    TakeActionProbability: int = Field(default_factory=generate_probability)
    # ActionSelectionWeights: List[None] = Field(default_factory=generate_weights)
    MakeMoveProbability: int = Field(default_factory=generate_probability)
    MoveSuccessProbability: int = Field(default_factory=generate_probability)
    BreedSuccessProbability: int = Field(default_factory=generate_probability)
    BreedActionProbability: int = Field(default_factory=generate_probability)
    # MoveDirectionDistribution: List[int] = Field(default_factory=generate_distribution(9))
    AwarenessScore: int = Field(default_factory=generate_score)
    # ActionOrderDistribution: List[int] = Field(default_factory=generate_distribution(3))
    ActionPrivilegeScore: int = Field(default_factory=generate_score)
    HappinessScore: int = Field(default_factory=generate_score)
    EnvironmentScore: int = Field(default_factory=generate_score)