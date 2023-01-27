import sys
import textwrap
from typing import Callable, NamedTuple


class Component(NamedTuple):
    package_name: str
    plugin_name: str
    func_name: str
    func: Callable
    description: str
    doc: str
    module_doc: str
    enabled: bool
        


# Dictionary with information about all registered plug-ins
#! will be a dict with key as the component name, value is a dict of components with...
#! the key as ??? and the values ???
_COMPONENTS = {}

COMPONENTS: Dict[str, Dict[str, Component]] = {}

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
            #! which ones can I get rid of
            package_name, _, plugin_name = func.__module__.rpartition(".")
            description, _, doc = (func.__doc__ or "").partition("\n\n")
            func_name = func.__name__
            module_doc = sys.modules[func.__module__].__doc__ or ""
            
            pkg_info = _COMPONENTS.setdefault(package_name, {})
            plugin_info = pkg_info.setdefault(plugin_name, {})
            plugin_info[func_name] = Component(
            package_name=package_name,
            plugin_name=plugin_name,
            func_name=func_name,
            func=func,
            description=description,
            doc=textwrap.dedent(doc).strip(),
            module_doc=module_doc,
            enabled=True
            )
                
            return func

        return inner_wrapper

    def get_components(self, type: str):
        return _COMPONENTS[type].values()
    
    def get_component(self, type: str, name: str):
        return _COMPONENTS[type][name].values()
    
    def get_component_dict(self, type: str, name: str):
        return _COMPONENTS[type][name]
    
    def get_components_dict(self, type: str):
        return _COMPONENTS[type]
    
    def get_func(self, type: str, name: str):
        return _COMPONENTS[type][name].func
    
    def get_funcs(self, type: str):
        return [x.func for x in _COMPONENTS[type].values()]
