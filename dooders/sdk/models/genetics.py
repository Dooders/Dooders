from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dooders.sdk.models.dooder import Dooder


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
        # genetics = Strategy.compile(dooder, GeneticStrategy)
        cls.genetic_profiles.append(genetics)

        return genetics

    @classmethod
    def combine_genetics(cls, dooder1: 'Dooder', dooder2: 'Dooder'):
        pass
