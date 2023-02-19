""" 
Move Action
-----------
This module contains the actions that allow dooders
to move around the environment.
"""

from sdk.core.action import Action
from sdk.core import Policy
from sdk.core.settings import Settings
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
    #! make it so Dooder object is assigned its own polices that can be referenced from the object
    #! it originally was getting the chosen movement policy from the simulation object
    chosen_policy = Settings.get('variables')['policies']['Movement'].args['value'] #! make this a lot simpler and cleaner
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
