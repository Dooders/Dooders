import yaml
from sdk.base.base_object import BaseObject
from sdk.strategies.strategies import BaseStrategy, compile_strategy, Strategies


BehaviorStrategy = Strategies.load_strategy('sdk/dooder/seed.yml')


class Behavior:
    """ 
    Behavior class used to generate the genetic expression of a Dooder
    A genetic expression is a set of probabilities and weights that determine 
    the behavior of a Dooder.
    """
        
    @classmethod
    def compile_genetics(cls, genetics: dict) -> dict:
        #! maybe add this part of the load strategy method
        #! might not even need this class at all???
        """ 
        Compile the genetics profiles

        Args:
            genetics (dict): The genetics profiles
        """
        full_results = {}
        for gene in GeneticStrategy:
            full_results[gene] = BaseStrategy(**GeneticStrategy[gene])
            
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

