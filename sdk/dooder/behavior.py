from random import randint, randrange, sample
from typing import Any, List

from pydantic import BaseModel, Field


class Fate:

    def __init__():
        pass


def generate_probability():
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
    
    
# class BaseBehavior(BaseModel):
#     ActionSuccessProbability: int = 0
#     TakeActionProbability: int = 0
#     ActionSelectionWeights: List = []
#     MakeMoveProbability: int = 0
#     MoveSuccessProbability: int = 0
#     BreedSuccessProbability: int = 0
#     BreedActionProbability: int = 0
#     MoveDirectionDistribution: List = []
#     AwarenessScore: int = 0
#     ActionOrderDistribution: List = []
#     ActionPrivilegeScore: int = 0
#     HappinessScore: int = 0
#     EnvironmentScore: int = 0


# class Behavior(BaseModel):
        
#         ActionSuccessProbability = generate_probability()
#         TakeActionProbability = generate_probability()
#         ActionSelectionWeights = generate_weights()
#         MakeMoveProbability = generate_probability()
#         MoveSuccessProbability = generate_probability()
#         BreedSuccessProbability = generate_probability()
#         BreedActionProbability = generate_probability()
#         MoveDirectionDistribution = generate_distribution(9)
#         AwarenessScore = generate_score()
#         ActionOrderDistribution = generate_distribution(3)
#         ActionPrivilegeScore = generate_score()
#         HappinessScore = generate_score()
#         EnvironmentScore = generate_score()


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