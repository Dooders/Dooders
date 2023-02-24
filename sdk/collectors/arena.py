""" 
Arena Collectors
-----------------
Collectors that are specific to the Arena.
"""

from sdk.core.core import Core


@Core.register('collector')
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

@Core.register('collector')
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

@Core.register('collector')
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
