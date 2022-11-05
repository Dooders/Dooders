""" 

"""

from typing import TYPE_CHECKING

from sdk.core import Condition, Fate

if TYPE_CHECKING:
    from sdk.core import Dooder


@Condition.register('starvation')
def starvation(dooder: 'Dooder') -> bool:
    """
    Check if the dooder is starving
    """

    # The higher the dooder's hunger, the more likely they are to starve
    probabilities = [0.05, 0.1, 0.2, 0.5, 0.75, 0.99]
    
    

    if dooder.hunger >= 1:
        return Fate.ask_fate(probabilities[dooder.hunger])
    else:
        return False
