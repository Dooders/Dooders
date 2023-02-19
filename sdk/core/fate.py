""" 
Fate module used to decide the "fate" of an action.
"""

from random import randint

class Fate:
    """ 
    Fate class used to decide the "fate" of an action.
    #! Do I need this class when I have strategies and conditions framework???
    #! or maybe have a fate strategy
    """
        
    @classmethod
    def ask_fate(cls, probability: int) -> bool:
        """ 
        Ask fate if the action is successful

        Args:
            probability: The probability of the action being successful.

        Returns:
            bool: True if the action is successful, False otherwise.
            
        #TODO: Determine different distributions to check against the supplied probability.
        """

        if randint(1, 100) < probability:
            return True
        else:
            return False
