""" 
Core: Condition
---------------
This module contains the Condition class,
which is used to register and check conditions.
"""

from sdk.core.core import Core


class Condition(Core):
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
    def check_conditions(cls, scope: str, *args, **kwargs) -> bool:
        #! need to figure out the design of this
        #! can't have both an object instance call to components and non instance like this
        #! most likely has to be singleton class based on Core
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
        for condition in cls.get_components('', 'sdk.conditions'):
            for value in condition.values():
                if value.plugin_name == scope:
                    func = value.func
                    if func(*args, **kwargs):
                        return True, condition
                return False, None
