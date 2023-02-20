""" 
Reproduction Condition
---------------
This condition is responsible for the tests required to 
check if a dooder can reproduce

"""

from typing import TYPE_CHECKING

from sdk.core import Condition

if TYPE_CHECKING:
    from sdk.core import Dooder

#! need to figure out how to deal with and/or conditions
@Condition.register('MinimumAge')
def minimum_age(dooder: 'Dooder') -> bool:
    """
    Check if the dooder is old enough to reproduce
    The dooder must be at least 5 cycles old to reproduce

    Parameters
    ----------
    dooder : Dooder
        The dooder to check

    Returns
    -------
    bool
        True if the dooder is old enough, False otherwise
    """
    if dooder.age >= 5:
        return True


@Condition.register('MinimumEnergy')
def minimum_energy(dooder: 'Dooder') -> bool:
    """
    Check if the dooder has enough energy to reproduce
    The dooder must have at least 50 energy to reproduce

    Parameters
    ----------
    dooder : Dooder
        The dooder to check

    Returns
    -------
    bool
        True if the dooder has enough energy, False otherwise
    """
    if dooder.hunger <= 1:
        return True
