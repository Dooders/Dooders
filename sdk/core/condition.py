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
    check(scope: str, *args, **kwargs) -> bool
        Checks if any of the registered conditions are met. 
    """

    @classmethod
    def check(cls, scope: str, *args, **kwargs) -> bool:
        """ 
        Check if any of the registered conditions are met.

        Parameters
        ----------
        scope : str, (simulation, dooder, etc.)
            The scope of the condition

        Returns
        -------
        bool
            True if any of the conditions are met.
            
        Examples
        --------
        >>> from sdk.core.condition import Condition
        >>>
        >>> Condition.check('simulation')
        False
        """
        registered_conditions = Core.get_components('sdk.conditions')

        for condition in registered_conditions[scope].values():
            function = condition.function
            if function(*args, **kwargs):
                return True, condition
            return False, None
