from sdk.actions import *
from sdk.strategies import *
from sdk.steps import *
from sdk.policies import *
from sdk.core.step import *
from sdk.core.core import _COMPONENTS
from sdk.core.settings import Settings

class Configure:
    """ 
    
    """
    
    @classmethod
    def settings(cls, type: str = None):
        """ Set a setting value """
        if type is None:
            return cls.options()
        else:
            return cls.options()[type]
    
    @classmethod
    def options(self) -> dict:
        """ Discover all core components and settings """
        return {
            'components': self.discover_components(),
            'variables': Variables.discover()
        }
    
    @classmethod
    def discover_components(self) -> dict:
        """ Discover all core component functions """
        component_options = {}

        for component, modules in _COMPONENTS.items():
            component_dict = {}

            for module, functions in modules.items():
                component_dict[module] = {}
                options = []

                for function in functions:
                    options.append(function)

                component_dict[module] = options

            component_options[component] = component_dict

        return component_options