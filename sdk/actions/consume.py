""" 
Consume Action
--------------
This module contains the actions that allow dooders 
to consume energy from the environment.
"""

from sdk.core.action import Action
from sdk.models.energy import Energy


@Action.register()
def consume(dooder) -> None:
    """ 
    Consume energy from the environment

    Parameters
    ----------
    dooder : Dooder
        The dooder that is consuming energy
    """
    cell_contents = dooder.simulation.environment.contents(dooder.position)
    energy = next((obj for obj in cell_contents if isinstance(obj, Energy)), None)
    
    if energy:
        energy.consume()
        dooder.hunger = 0
        dooder.energy_consumed += 1
        dooder.log(
            granularity=2, message=f"Consumed energy: {energy.id}", scope='Dooder')
    else:
        dooder.hunger += 1
