""" 
Resources collectors
--------------------
Collectors for resources.
"""

from sdk.core.collector import Collector


@Collector.register()
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

    return len(simulation.resources.available_resources)


@Collector.register()
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

    return simulation.resources.consumed_energy


@Collector.register()
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

    return simulation.resources.allocated_energy
