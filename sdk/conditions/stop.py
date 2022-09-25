""" 

"""

from typing import TYPE_CHECKING

from sdk.conditions.conditions import Conditions

if TYPE_CHECKING:
    from sdk import Simulation


@Conditions.register('check_max_cycle')
def check_max_cycle(simulation: 'Simulation') -> bool:
    """ 
    Check if the maximum number of cycles has been reached.
    """
    if simulation.cycles >= simulation.params.Simulation.MaxCycles:
        return True


@Conditions.register('check_simulation_running')
def check_simulation_running(simulation: 'Simulation') -> bool:
    """ 
    Check if the simulation is still running.
    """
    if not simulation.running:
        return True


@Conditions.register('check_dooder_count')
def check_dooder_count(simulation: 'Simulation') -> bool:
    """ 
    Check if the number of dooders has reached zero.
    """
    if len(simulation.environment.get_objects("Dooder")) == 0:
        return True