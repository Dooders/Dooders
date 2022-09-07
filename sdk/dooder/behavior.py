from enum import Enum
from functools import partial
from random import randint, randrange, sample
from typing import Any, List
import yaml

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
    
    
class Generators:
    Probability = generate_probability
    Distribution = generate_distribution
    Weights = generate_weights
    Score = generate_score

class Behavior(BaseModel):
    ActionSuccessProbability: int = 0
    TakeActionProbability: int = 0
    ActionSelectionWeights: List[int] = []
    MakeMoveProbability: int = 0
    MoveSuccessProbability: int = 0
    BreedSuccessProbability: int = 0
    BreedActionProbability: int = 0
    MoveDirectionDistribution: List[int] = []
    ActionOrderDistribution: List[int] = []


def load_behavior_profiles():
    with open('sdk/dooder/genetics.yml') as f:
        profile = yaml.load(f, Loader=yaml.FullLoader)
        return profile

def generate_values(profile):
    generated_values = {}
    for key, value in profile.items():

        if type(value['Generator']) == list:
            generator = getattr(Generators, value['Generator'][0])
            generator_func = partial(generator, value['Generator'][1])
            
        else:
            generator_func = getattr(Generators, value['Generator'])
            
        generated_values[key] = generator_func()
        
    return generated_values
    
def generate_behavior():
    profile = load_behavior_profiles()
    values = generate_values(profile)
    return Behavior(**values)


print(generate_behavior())