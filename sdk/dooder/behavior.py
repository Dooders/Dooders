import yaml
from sdk.base.base_object import BaseObject
from sdk.strategies.strategies import BaseStrategy, compile_strategy



class Behavior:
    """ 
    Behavior class used to generate the genetic expression of a Dooder
    A genetic expression is a set of probabilities and weights that determine 
    the behavior of a Dooder.
    """

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
    def compile_genetics(cls, genetics: dict) -> dict:
        """ 
        Compile the genetics profiles

        Args:
            genetics (dict): The genetics profiles
        """
        full_results = {}
        for gene in genetics:
            full_results[gene] = BaseStrategy(**genetics[gene])
            
        return full_results
    
    
    @classmethod
    def generate_behavior(cls, dooder: BaseObject) -> dict:
        """ 
        Generate a behavior profile for a Dooder

        Returns:
            BehaviorProfile: The behavior profile for a Dooder based on genetics
        """

        genetics = cls.load_genetics()
        behavior_profiles = cls.compile_genetics(genetics)
        compile_strategy(dooder, behavior_profiles)
        
        return behavior_profiles

