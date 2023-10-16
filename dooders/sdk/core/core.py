""" 
Core module for the SDK

This module contains the Core class, which is used to register plug-ins.
"""

from abc import ABC
import logging
import os
from typing import Callable, Dict, NamedTuple

logger = logging.getLogger(__name__)


class Component(NamedTuple):
    component_name: str
    folder_name: str
    file_name: str
    function_name: str
    function: Callable
    description: str
    enabled: bool


# Dictionary with information about all registered plug-ins
# Example _COMPONENTS dictionary entry
# {'actions': {'consume': {'consume': Component}}}
_COMPONENTS: Dict[str, Dict[str, Dict[str, Component]]] = {}


class Core(ABC):
    """
    Base class to be inherited by core components to facilitate plug-in like usage
    of sub-components.

    Attributes
    ----------
    _COMPONENTS: Dict[str, Dict[str, Dict[str, Component]]]
        A dictionary with information about all registered plug-ins.
        Example: {'actions': {'consume': {'consume': Component}}}

    Methods
    -------
    register(*args, **kwargs) -> Callable
        Register a collector in the registry.
    get_components(component: str) -> Dict[str, Dict[str, Component]]
        Get all components of a certain type.
    get_component(component: str, name: str) -> Dict[str, Component]
        Get a component of a certain type.

    Examples
    --------
    * Register a function as a plug-in
    >>> from sdk.core.core import Core
    >>>
    >>> @Core.register()
    >>> def my_function():
    >>>     pass
    * Get all components of a certain type
    >>> from sdk.core.core import Core
    >>>
    >>> Core.get_components('actions')
    {'actions': {'consume': {'consume': <Component>}}}
    * Get a component of a certain type
    >>> from sdk.core.core import Core
    >>>
    >>> Core.get_component('actions', 'consume')
    {'consume': <Component>}
    """

    enable_logging = os.getenv("ENABLE_LOGGING", "False").lower() == "true"

    @classmethod
    def register(cls, component_name: str, *args, **kwargs) -> Callable:
        """
        Register a collector in the registry.

        Parameters
        ----------
        component_name: str
            The name of the component to register.

        Example
        -------
        >>> from sdk.core.core import Core
        >>>
        >>> @Core.register()
        >>> def my_function():
        >>>     pass
        """

        def inner_wrapper(func: Callable) -> Callable:
            folder_name, _, file_name = func.__module__.rpartition(".")
            description, _, _ = (func.__doc__ or "").partition("\n\n")
            function_name = func.__name__

            pkg_info = _COMPONENTS.setdefault(component_name, {})
            plugin_info = pkg_info.setdefault(file_name, {})
            plugin_info[function_name] = Component(
                component_name=component_name,
                folder_name=folder_name,
                file_name=file_name,
                function_name=function_name,
                function=func,
                description=description,
                enabled=True,
            )

            if cls.enable_logging:
                # Log the registration of the plugin
                logger.info(
                    f"Registered plugin '{function_name}' in component '{component_name}'"
                )

            return func

        return inner_wrapper

    @classmethod
    def get_components(cls, component_name: str) -> Dict[str, Dict[str, Component]]:
        """
        Get all components of a certain type.

        Parameters
        ----------
        component_name: str
            The type of component to get.
            Example: 'actions', 'collectors', etc.

        Returns
        -------
        components: Dict[str, Dict[str, Component]]
            A dictionary of all components of the specified type.

        Examples
        --------
        >>> from sdk.core.core import Core
        >>>
        >>> Core.get_components('actions')
        {'actions': {'consume': {'consume': <Component>}}}
        """
        return _COMPONENTS[component_name]

    @classmethod
    def get_component(
        csl, component_name: str, function_name: str
    ) -> Dict[str, Component]:
        """
        Get a component of a certain type.

        Parameters
        ----------
        component_name: str
            The type of component to get.
            Example: 'actions', 'collectors', etc.
        function_name: str
            The name of the component to get.
            Example: 'consume', 'move', etc.

        Returns
        -------
        component: Dict[str, Component]
            A dictionary of the component of the specified type.

        Examples
        --------
        >>> from sdk.core.core import Core
        >>>
        >>> Core.get_component('actions', 'consume')
        {'consume': <Component>}
        """
        try:
            component_dict = _COMPONENTS[component_name]
            return component_dict[function_name]
        except KeyError as e:
            raise KeyError(f"Component not found: {e}") from None
