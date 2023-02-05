""" 
Settings
--------
This module contains the settings class for the SDK.
"""

from typing import Dict

from sdk.core import Strategy
from sdk.core.variables import Variables
from sdk.core.core import _COMPONENTS


EXAMPLE_SETTINGS = {}


class Settings:
    
    settings = {}
    
    def __init__(self, settings: dict = {}):
        self.update(settings)
    
    def update(self, settings):
        """ Compile a settings object from a dictionary """
        self.settings['variables'] = self.update_variables(settings)
        self.settings['components'] = self.update_components(settings)
        
    def update_components(self, settings):
        """ Update component settings """
        final_components = {}
        for component, modules in _COMPONENTS.items():
            for module, functions in modules.items():
                for function in functions:
                    if function in settings:
                        final_components[function] = settings[function]
                    else:
                        final_components[function] = function
                        
        return final_components
    
    def update_variables(self, settings):
        """ Update variable settings """
        #! missing the model as a key like in components
        variable_dict = Variables.discover()
        final_variables = {}
        for variables in variable_dict.values():
            for variable in variables:
                if variable.name in settings:
                    final_variables[variable.name] = settings[variable.name]
                else:
                    final_variables[variable.name] = variable.default
                    
        return final_variables
    
    def compile(self, name):
        #! clean up the Strategy class
        strategies = Strategy.dict()
        pass
    
    def get(self, model: str) -> 'Settings':
        """ Get a setting """
        return self.settings[model]