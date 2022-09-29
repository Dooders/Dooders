""" 

"""

from typing import TYPE_CHECKING

from sdk.core import Condition

if TYPE_CHECKING:
    from sdk.dooder import Dooder


@Condition.register('starvation')
def starvation(dooder: 'Dooder') -> bool:
    #! maybe have a process that you supply attribute and default value, and if it doesnt exsist in the dooder object, it creates it
    # create a days hungry attribute if it doesn't exist
    if not hasattr(dooder, 'days_hungry'):
        dooder.days_hungry = 0

    # if the dooder is hungry, increment the days hungry attribute
    if dooder.energy_supply <= 0:
        dooder.days_hungry += 1
    else:
        dooder.days_hungry = 0

    # if the dooder has been hungry for 3 days, return true
    if dooder.days_hungry >= 3:
        return True
    else:
        return False
