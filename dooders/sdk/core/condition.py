""" 
Core: Condition
---------------
This module contains the Condition class,
which is used to register and check conditions.
"""

from dooders.sdk.core.core import Core


class Condition(Core):
    """ 
    The factory class to be used as a decorator to register a stop condition.

    Methods
    -------
    check(scope: str, *args, **kwargs) -> bool
        Checks if any of the registered conditions are met. 
    """
    
    _registered_conditions = None
    
    @classmethod
    def _build(cls):
        pass
    
    @classmethod
    def _get_registered_conditions(cls):
        if cls._registered_conditions is None:
            cls._registered_conditions = Core.get_components('condition')
        return cls._registered_conditions
    
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
        
        """
        registered_conditions = cls._get_registered_conditions()
        
        if scope not in registered_conditions:
            raise ValueError(f"Invalid scope: {scope}")
        
        for condition in registered_conditions[scope].values():
            if not callable(condition.function):
                raise TypeError("Condition function is not callable")
            result, reason = cls.execute_methods(condition.function, *args, **kwargs)
            return result, reason

        return False, None
        
    @classmethod
    def execute_methods(cls, condition, model):
        """
        Execute all public methods of an object that do not start with an underscore.

        Args:
            obj: An instance of a class.
            model: The model to pass as an argument to the methods.

        Returns:
            A tuple containing a boolean indicating whether all/any methods returned True, 
            and a list of method names that failed (if any).
        """
        results = []
        failed_methods = []
        operator = condition.__dict__.get('_OPERATOR', 'all') # default to 'all' if _OPERATOR attribute is not found
        for name in dir(condition):
            if not name.startswith('_'):
                attr = getattr(condition, name)
                if callable(attr):
                    results.append(attr(model))
                    if not attr(model):
                        failed_methods.append(name)

        if operator == 'all':
            if all(results):
                return True, None
            else:
                return False, failed_methods[0]
                    
        if operator == 'any':
            if any(results):
                return True, None
            else:
                return False, None
            