""" 
Move Action
-----------
This module contains the actions that allow dooders
to move around the environment.
"""

from sdk.core.action import Action
from sdk.core import Policy
from sdk.utils.get_direction import get_direction


@Action.register()
def move(dooder) -> None:
    """ 
    Move the dooder to a new cell in the environment

    Parameters
    ----------
    dooder : Dooder
        The dooder that is moving
    """
    policy = dooder.simulation.params.get('Policies').Movement
    destination = Policy.execute(policy, dooder)

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
