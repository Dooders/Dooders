from functools import partial
from typing import List

import yaml
from pydantic import BaseModel
from sdk.dooder.fate import Fate


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
    """ 
    Behavior class used to generate the genetic expression of a Dooder
    A genetic expression is a set of probabilities and weights that determine 
    the behavior of a Dooder.
    """
    
    behavior_profiles = []

    @classmethod
    def load_genetics(self) -> dict:
        """ 
        Load the genetics from the yaml file

        Returns:
            dict: The genetics profiles
        """

        with open('sdk/dooder/genetics.yml') as f:
            genetics = yaml.load(f, Loader=yaml.FullLoader)

            return genetics

    @classmethod
    def generate_values(self, genetics: dict) -> dict:
        """ 
        Generate the values for the behavior profile

        Args:
            genetics: The genetics profiles

        Returns:
            dict: The values for the behavior profile
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
        Generate a behavior profile for a Dooder

        Returns:
            BehaviorProfile: The behavior profile for a Dooder based on genetics
        """

        genetics = cls.load_genetics()
        profile = cls.generate_values(genetics)
        behavior = BehaviorProfile(**profile)
        cls.behavior_profiles.append(behavior)

        return behavior
