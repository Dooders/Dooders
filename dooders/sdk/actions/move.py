""" 
Move Action
-----------
This module contains the actions that allow dooders
to move around the environment.
"""

import random

import numpy as np

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
    reality_array = dooder.perception.array('Energy')
    sensory_array = Senses.gather(dooder)
    fixed_array = np.where(sensory_array >= 0.5, 1, 0)
    # print(f'Sensory Array: {sensory_array}')
    # print(f'Fixed Array: {fixed_array}')
    # print(f'Reality Array: {reality_array}')
    # print('******************')
    destination = dooder.think('move_decision', fixed_array, reality_array)

    if isinstance(destination, np.int64):
        final_destination = destination
    elif isinstance(destination, np.ndarray) and len(destination) > 0:
        final_destination = destination.argmax()
    elif isinstance(destination, (list, np.ndarray)) and len(destination) > 0:
        final_destination = random.choice([d for d in destination if d != 0])
    else:
        raise ValueError(f"Destination {destination} is not valid")

    coordinates = dooder.perception.coordinates[final_destination]

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
