""" 
Core: Condition
---------------
This module contains the Condition class,
which is used to register and check conditions.
"""

from sdk.core import CoreComponent


class Condition(CoreComponent):
    """ 
    The factory class to be used as a decorator to register a stop condition.

    Methods
    -------
    register
        Registers a stop condition to the Condition class.
    check_conditions
        Checks if any of the registered conditions are met. 
    """

    @classmethod
    def check(cls, scope: str, *args, **kwargs) -> bool:
        """ 
        Check if any of the registered conditions are met.

        Parameters
        ----------
        simulation: Simulation
            The simulation to check the conditions for.

        Returns
        -------
        bool
            True if any of the conditions are met.
        """
        registered_conditions = Core.get_components('sdk.conditions')

        for condition in registered_conditions[scope].values():
            function = condition.function
            if function(*args, **kwargs):
                return True, condition
            return False, None
