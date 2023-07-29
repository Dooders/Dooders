""" 
Stop Conditions
----------------
Determined when the simulation should stop.
"""

from typing import TYPE_CHECKING

from dooders.sdk.core.core import Core

if TYPE_CHECKING:
    from dooders.sdk import Simulation


@Core.register('condition')
class StopConditions:

    _OPERATOR = 'any'

    @classmethod
    def max_cycle(cls, simulation: 'Simulation') -> bool:
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
        if simulation.cycle_number >= simulation.settings.get('MaxCycles'):
            return True

    @classmethod
    def simulation_running(cls, simulation: 'Simulation') -> bool:
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

    @classmethod
    def dooder_count(cls, simulation: 'Simulation') -> bool:
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
        if len(list(simulation.environment.get_objects("Dooder"))) == 0:
            return True
