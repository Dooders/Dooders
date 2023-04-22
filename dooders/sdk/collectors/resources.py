""" 
Resources collectors
--------------------
Collectors for resources.
"""

from dooders.sdk.core.core import Core


@Core.register('collector')
def available_energy(simulation) -> int:
    """ 
    The amount of available energy.

    Parameters
    ----------
    simulation : Simulation
        The simulation to check

    Returns
    -------
    int
        The amount of available energy
    """

    return 'available_energy', len(simulation.resources.available_resources)


@Core.register('collector')
def consumed_energy(simulation) -> int:
    """ 
    The amount of consumed energy.

    Parameters
    ----------
    simulation : Simulation
        The simulation to check

    Returns
    -------
    int
        The amount of consumed energy
    """

    return 'consumed_energy', simulation.resources.consumed_energy


@Core.register('collector')
def allocated_energy(simulation) -> int:
    """ 
    The amount of allocated energy.

    Parameters
    ----------
    simulation : Simulation 
        The simulation to check

    Returns
    -------
    int
        The amount of allocated energy
    """

    return 'allocated_energy', simulation.resources.allocated_energy
