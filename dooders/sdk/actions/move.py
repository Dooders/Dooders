""" 
Move Action
-----------
This module contains the actions that allow dooders
to move around the environment.
"""

from dooders.sdk.core.core import Core
from dooders.sdk.models.senses import Senses
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
    """

    sensory_array = Senses.gather(dooder)
    
    # print(f"Sensory Array: {sensory_array}")

    destination = dooder.think('move_decision', sensory_array)
    
    # print(f"Destination: {destination}")
    
    coordinates = dooder.perception.coordinates[destination]
    
    # print(f'Coordinates: {coordinates}')
    #! I'm not giving the model its full potential. Give the moved_decision the perception array too. It needs that information to make a decision.

    if coordinates == dooder.position:
        pass
    else:
        origin = dooder.position
        dooder.direction = get_direction(origin, coordinates)
        dooder.simulation.environment.move_object(dooder, coordinates)
        dooder.move_count += 1

        dooder.log(granularity=2,
                   message=f"Moved {dooder.direction} from {origin} to {coordinates}",
                   scope='Dooder')

        dooder.position = coordinates
