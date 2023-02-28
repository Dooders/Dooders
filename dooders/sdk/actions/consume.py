""" 
Consume Action
--------------
This module contains the actions that allow dooders 
to consume energy from the environment.
"""

from dooders.sdk.core.core import Core
from dooders.sdk.models.energy import Energy


@Core.register('action')
def consume(dooder) -> None:
    """ 
    Consume energy from the environment

    Function will look for energy in the cell that the dooder is in, and
    consume it if it exists. If the dooder is not in a cell with energy,
    the dooder's hunger will increase.

    Parameters
    ----------
    dooder : Dooder
        The dooder that is consuming energy

    Examples
    --------
    >>> dooder = Dooder((0, 0))
    >>> dooder.simulation.environment.add(Energy(), (0, 0))
    >>> Action.execute(dooder, 'consume')
    >>> dooder.energy
    1
    """
    cell_contents = dooder.simulation.environment.contents(dooder.position)
    energy = next(
        (obj for obj in cell_contents if isinstance(obj, Energy)), None)

    if energy:
        energy.consume()
        dooder.hunger = 0
        dooder.energy_consumed += 1
        dooder.log(
            granularity=2, message=f"Consumed energy: {energy.id}", scope='Dooder')
    else:
        dooder.hunger += 1
