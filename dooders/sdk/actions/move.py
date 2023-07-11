""" 
Move Action
-----------
This module contains the actions that allow dooders
to move around the environment.
"""

from dooders.sdk.core import Policy
from dooders.sdk.core.core import Core
from dooders.sdk.core.settings import Settings
from dooders.sdk.utils.get_direction import get_direction


@Core.register('action')
def move(dooder) -> None:
    """ 
    Move the dooder to a new cell in the environment

    Function will look for a policy in the settings that will determine
    where the dooder will move to. If the dooder is not able to move to
    the cell, the dooder's move count will not increase.

    Parameters
    ----------
    dooder : Dooder
        The dooder that is moving

    Examples
    --------
    >>> dooder = Dooder((0, 0))
    >>> Action.execute(dooder, 'move')
    >>> dooder.position
    (0, 1)
    """
    chosen_policy = Settings.search('Movement')
    destination = Policy.execute(chosen_policy, dooder)

    if destination == dooder.position:
        pass
    else:
        origin = dooder.position
        dooder.direction = get_direction(origin, destination)
        dooder.simulation.environment.move_object(dooder, destination)
        dooder.move_count += 1
        dooder.log(
            granularity=2, message=f"Moved {dooder.direction} from {origin} to {destination}", scope='Dooder')
        dooder.position = destination
