""" 
Core module for the SDK
"""

from typing import Callable, Dict, NamedTuple

#! need to make sure every component is loaded before simulation starts

class Component(NamedTuple):
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

class Core:

    @classmethod
    def register(cls, *args, **kwargs) -> Callable:
        """ 
        Register a collector in the registry.

        Returns
        -------
        inner_wrapper: Callable
            The decorator function.
        """

        def inner_wrapper(func: Callable) -> Callable:
            folder_name, _, file_name = func.__module__.rpartition(".")
            description, _, _ = (func.__doc__ or "").partition("\n\n")
            function_name = func.__name__
            
            pkg_info = _COMPONENTS.setdefault(folder_name, {})
            plugin_info = pkg_info.setdefault(file_name, {})
            plugin_info[function_name] = Component(
            folder_name=folder_name,
            file_name=file_name,
            function_name=function_name,
            function=func,
            description=description,
            enabled=True
            )
                
            return func

        return inner_wrapper

    @classmethod
    def get_components(self, component: str) -> Dict[str, Dict[str, Component]]:
        """ 
        Get all components of a certain type.

        Parameters
        ----------
        component: str
            The type of component to get.

        Returns
        -------
        components: Dict[str, Dict[str, Component]]
            A dictionary of all components of the specified type.
        """
        return _COMPONENTS[component]
    
    @classmethod
    def get_component(self, component: str, name: str) -> Dict[str, Component]:
        """ 
        Get a component of a certain type.

        Parameters
        ----------
        component: str
            The type of component to get.
        name: str
            The name of the component to get.

        Returns
        -------
        component: Dict[str, Component]
            A dictionary of the component of the specified type.
        """
        return _COMPONENTS[component][name]
    
    # def get_component_dict(self, type: str, name: str):
    #     return _COMPONENTS[type][name]
    
    # def get_components_dict(self, type: str):
    #     return _COMPONENTS[type]
    
    # def get_func(self, type: str, name: str):
    #     return _COMPONENTS[type][name].func
    
    # def get_funcs(self, type: str):
    #     return [x.func for x in _COMPONENTS[type].values()]
