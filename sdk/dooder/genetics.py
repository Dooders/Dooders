from typing import TYPE_CHECKING

from sdk.core.strategy import Strategies, compile_strategy

if TYPE_CHECKING:
    from sdk.dooder.dooder import Dooder

GeneticStrategy = Strategies.load_strategy('sdk/dooder/genetics.yml')


class Genetics:
    """ 
    
    """

    genetic_profiles = []

    @classmethod
    def compile_genetics(cls, dooder: 'Dooder') -> dict:
        """ 
        Compile the genetics of a dooder.
        
        Args:
            dooder: The dooder to compile the genetics for.
        
        Returns:
            The compiled genetics.
        """
        genetics = compile_strategy(dooder, GeneticStrategy)
        cls.genetic_profiles.append(genetics)

        return genetics

    @classmethod
    def combine_genetics(cls, dooder1: 'Dooder', dooder2: 'Dooder'):
        pass
