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
    
    _registered_conditions = None
    _condition_cache = {}
    
    @classmethod
    def _get_registered_conditions(cls):
        if cls._registered_conditions is None:
            cls._registered_conditions = Core.get_components('sdk.conditions')
        return cls._registered_conditions
    
    @classmethod
    def _check(self, conditions, *args, **kwargs) -> bool:
        """ 
        Check if the condition is met.

        Parameters
        ----------
        *args, **kwargs
            The arguments to be passed to the function.

        Returns
        -------
        bool
            True if the condition is met, False otherwise.
        """
        for condition_dict in conditions.values():
            for condition in condition_dict.values():
                function = condition.function
                if function(*args, **kwargs):
                    return True, condition
                return False, None

    @classmethod
    def check_new(cls, scope: str, *args, **kwargs) -> bool:
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
        
        """
        registered_conditions = cls._get_registered_conditions()
        
        if scope not in registered_conditions:
            raise ValueError(f"Invalid scope: {scope}")
        
        for condition in registered_conditions[scope].values():
            if not callable(condition.function):
                raise TypeError("Condition function is not callable")
            if condition.function(*args, **kwargs):
                return True, condition.function_name

        return False, None

        # if scope in cls._condition_cache.keys():
        #     conditions = cls._condition_cache.get(scope)
        
        # elif scope not in cls._condition_cache:
        #     conditions = Core.get_components('sdk.conditions')
        #     cls._condition_cache[scope] = conditions[scope]
        
        # return cls._check(conditions, *args, **kwargs)
    
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