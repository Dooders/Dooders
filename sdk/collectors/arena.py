""" 
Arena Collectors
-----------------
Collectors that are specific to the Arena.
"""

from sdk.core.collector import Collector


@Collector.register()
def active_dooder_count(simulation) -> int:
    """
    Return the number of dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    int
        The number of dooders in the simulation.
    """
    return simulation.arena.active_dooder_count

@Collector.register()
def terminated_dooder_count(simulation) -> int:
    """
    Return the number of dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    int
        The number of dooders in the simulation.
    """
    return simulation.arena.dooders_died

@Collector.register()
def created_dooder_count(simulation) -> int:
    """
    Return the number of dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    int
        The number of dooders in the simulation.
    """
    return simulation.arena.dooders_created
