""" 
Core: Surface
-------------
This module contains the Surface class.

A surface holds the objects in the environment 
based on the space type, like a gird
"""

import importlib
from abc import abstractmethod

from dooders.sdk.core.core import Core
from dooders.sdk.core.settings import Settings


class Surface(Core):
    """ 
    Surface class for the SDK. To be used inside the Environment class.

    This class is used to register surfaces and provide a schema for all surfaces.

    Methods
    -------
    build(surface_type: str) -> object
        Build a surface of a certain type.

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

        Raises
        ------
        ValueError
            If the requested surface type is not valid.

        Examples
        --------
        * Build a surface of a certain type
        >>> from sdk.core.surface import Surface
        >>>
        >>> surface = Surface.build('grid')
        """
        try:
            module = f'dooders.sdk.surfaces.{surface_type}'
            chosen_surface = getattr(
                importlib.import_module(module), surface_type.title())
            settings = Settings.get('variables', surface_type)
            final_settings = {k: v.args['value']
                              for k, v in settings.items() if v is not None}
            return chosen_surface(final_settings)
        except AttributeError:
            raise ValueError(f"Invalid surface type '{surface_type}'")

    # @abstractmethod
    # def test_dude(self):
    #     """Just some test method."""
    #     raise NotImplementedError('Must implement method test_dude')
