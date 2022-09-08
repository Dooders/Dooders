from functools import partial
from random import randint, randrange, sample
from typing import List

import yaml
from pydantic import BaseModel


class Fate:
    @classmethod
    def generate_probability(cls) -> int:
        """  
        
        """
        return randrange(1, 100)

    @classmethod
    def generate_weights(cls) -> List[int]:
        """ 
        
        """
        return [None]

    @classmethod
    def generate_score(cls) -> int:
        """ 
        
        """
        return randrange(1, 100)

    @classmethod
    def generate_distribution(cls, number_of_choices: int) -> List[int]:
        """
        Generates a distribution of probabilities for a given number of choices.
        """
        #! TODO: apply different distributions
        # random distribution
        dividers = sorted(sample(range(1, 100), number_of_choices - 1))
        return [a - b for a, b in zip(dividers + [100], [0] + dividers)]

    @classmethod
    def ask_fate(cls, probability: int) -> bool:
        """ 
        
        """
        if randint(1, 100) < probability:
            return True
        else:
            return False


class Generators:
    Probability = Fate.generate_probability
    Distribution = Fate.generate_distribution
    Weights = Fate.generate_weights
    Score = Fate.generate_score
        

class BehaviorProfile(BaseModel):
    ActionSuccessProbability: int = 0
    TakeActionProbability: int = 0
    ActionSelectionWeights: List[int] = []
    MakeMoveProbability: int = 0
    MoveSuccessProbability: int = 0
    BreedSuccessProbability: int = 0
    BreedActionProbability: int = 0
    MoveDirectionDistribution: List[int] = []
    ActionOrderDistribution: List[int] = []


class Behavior:

    @classmethod
    def load_genetics(self) -> dict:
        """ 
        
        """
        with open('sdk/dooder/genetics.yml') as f:
            genetics = yaml.load(f, Loader=yaml.FullLoader)
            return genetics

    @classmethod
    def generate_values(self, genetics: dict) -> dict:
        """ 
        
        """
        generated_values = {}
        for key, value in genetics.items():

            if type(value['Generator']) == list:
                generator = getattr(Generators, value['Generator'][0])
                generator_func = partial(generator, value['Generator'][1])

            else:
                generator_func = getattr(Generators, value['Generator'])

            generated_values[key] = generator_func()

        return generated_values

    @classmethod
    def generate_behavior(cls) -> BehaviorProfile:
        """ 
        
        """
        genetics = cls.load_genetics()
        profile = cls.generate_values(genetics)
        
        return BehaviorProfile(**profile)