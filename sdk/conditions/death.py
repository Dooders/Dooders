""" 
Death Condition
---------------
This condition is responsible for the tests required to 
trigger a 'death' status

"""

from typing import TYPE_CHECKING

from sdk.core import Condition, Fate

if TYPE_CHECKING:
    from sdk.core import Dooder


@Condition.register('Starvation')
def starvation(dooder: 'Dooder') -> bool:
    """
    Check if the dooder is starving
    
    The higher the dooder's hunger, the more likely they are to starve
    Each cycle in a hunger state increases the chance of death in a 
    check of Fate
    
    Parameters
    ----------
    dooder : Dooder
        The dooder to check
        
    Returns
    -------
    bool
        True if the dooder is starved to death, False otherwise
    """

    # The higher the dooder's hunger, the more likely they are to starve
    # TODO make the probabilities a setting
    probabilities = [0, 1, 2, 3, 20, 30, 50]
    
    if dooder.hunger >= 1 and dooder.hunger < 5:
        return Fate.ask_fate(probabilities[dooder.hunger])
    elif dooder.hunger >= 5:
        return Fate.ask_fate(probabilities[-1])
    else:
        return False
