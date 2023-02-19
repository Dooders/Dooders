""" 
Core: Surface
-------------
This module contains the Surface class.
"""

from abc import abstractmethod
from sdk.core import CoreComponent
from sdk.core.settings import Settings
import importlib


class Surface(CoreComponent):
    """ 
    Surface class for the SDK. To be used inside the Environment class.
    
    This class is used to register surfaces and provide a schema for all surfaces.
    
    Methods
    -------
    build(surface_type: str) -> object
        Build a surface of a certain type.
    test_dude(self), required
        Test method.
        
    See Also
    --------
    sdk.surfaces.grid.Grid: Grid surface class.
    sdk.models.environment.Environment: Environment class.
    
    Examples
    --------
    * Build a surface of a certain type
    >>> from sdk.core.surface import Surface
    >>>
    >>> surface = Surface.build('grid')
    """

    @classmethod
    def build(cls, surface_type: str) -> object:
        """ 
        Build a surface of a certain type.
        
        Parameters
        ----------
        surface_type: str
            The type of surface to build.
            Example: 'grid'
        
        Returns
        -------
        chosen_surface: object
            The Surface object.
        
        Examples
        --------
        * Build a surface of a certain type
        >>> from sdk.core.surface import Surface
        >>>
        >>> surface = Surface.build('grid')
        """
        module = f'sdk.surfaces.{surface_type}'
        chosen_surface = getattr(importlib.import_module(module), surface_type.title())
        settings = Settings.get('variables', surface_type)
        #! should clean up code below, or the process of getting settings
        final_settings = {k: v.args['value'] for k, v in settings.items() if v is not None}
        return chosen_surface(final_settings)
    
    @abstractmethod
    def test_dude(self):
        """Just some test method."""
        raise NotImplementedError('Must implement method test_dude')
