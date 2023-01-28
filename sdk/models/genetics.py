from typing import TYPE_CHECKING

from sdk.core import Strategy

if TYPE_CHECKING:
    from sdk.models.dooder import Dooder

GeneticStrategy = Strategy.load('genetics')


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
        genetics = Strategy.compile(dooder, GeneticStrategy)
        cls.genetic_profiles.append(genetics)

        return genetics

    @classmethod
    def combine_genetics(cls, dooder1: 'Dooder', dooder2: 'Dooder'):
        pass
