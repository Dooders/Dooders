""" 
Arena Collectors
-----------------
Collectors that are specific to the Arena.
"""

from dooders.sdk.core.core import Core

#! i can make collectors pass the specific model they want to collect from

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
    #! does this method need to just be a collector? 
    #! Are these 3 attributes used inside the code.
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

@Core.register('collector')
def average_dooder_age(simulation) -> float:
    """
    Return the average age of dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    float
        The average age of dooders in the simulation.
    """
    dooder_ages = [dooder.age for dooder in simulation.arena.dooders()]
    
    if len(dooder_ages) == 0:
        return 0
    else:
        return sum(dooder_ages) / len(dooder_ages)
    
@Core.register('collector')
def median_dooder_age(simulation) -> float:
    """
    Return the median age of dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    float
        The median age of dooders in the simulation.
    """
    dooder_ages = [dooder.age for dooder in simulation.arena.dooders()]
    
    if len(dooder_ages) == 0:
        return 0
    else:
        return sorted(dooder_ages)[len(dooder_ages) // 2]
    
@Core.register('collector')
def average_dooder_hunger(simulation) -> float:
    """
    Return the average hunger of dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    float
        The average hunger of dooders in the simulation.
    """
    dooder_hunger = [dooder.hunger for dooder in simulation.arena.dooders()]
    
    if len(dooder_hunger) == 0:
        return 0
    else:
        return sum(dooder_hunger) / len(dooder_hunger)
    
@Core.register('collector')
def average_energy_consumed(simulation) -> float:
    """
    Return the average energy consumed by dooders in the simulation.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to collect data from.
        
    Returns
    -------
    float
        The average energy consumed by dooders in the simulation.
    """
    dooder_energy_consumed = [dooder.energy_consumed for dooder in simulation.arena.dooders()]
    
    if len(dooder_energy_consumed) == 0:
        return 0
    else:
        return sum(dooder_energy_consumed) / len(dooder_energy_consumed)