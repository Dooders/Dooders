""" 
Stop Conditions
----------------
Determined when the simulation should stop.
"""

from typing import TYPE_CHECKING

from sdk.core import Condition

if TYPE_CHECKING:
    from sdk import Simulation


@Condition.register('Max cycles')
def check_max_cycle(simulation: 'Simulation') -> bool:
    """ 
    Check if the maximum number of cycles has been reached.
    
    The maximum number of cycles is defined in the simulation parameters.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to check
        
    Returns
    -------
    bool
        True if the maximum number of cycles has been reached, False otherwise
    """
    if simulation.cycles >= simulation.params.Simulation.MaxCycles:
        return True


@Condition.register('Simulation stopped')
def check_simulation_running(simulation: 'Simulation') -> bool:
    """ 
    Check if the simulation is still running.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to check
        
    Returns
    -------
    bool
        True if the simulation is not running, False otherwise
    """
    if not simulation.running:
        return True


@Condition.register('No more Dooders')
def check_dooder_count(simulation: 'Simulation') -> bool:
    """ 
    Check if the number of dooders has reached zero.
    
    Parameters
    ----------
    simulation : Simulation
        The simulation to check
        
    Returns
    -------
    bool
        True if the number of dooders has reached zero, False otherwise
    """
    if len(simulation.environment.get_objects("Dooder")) == 0:
        return True
