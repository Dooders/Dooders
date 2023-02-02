""" 
Settings
--------
This module contains the settings class for the SDK.
"""

from typing import Dict

from sdk.core import Strategy
from sdk.core.variables import Variables
from sdk.core.core import _COMPONENTS

#! no need to store instance of this anymore
#! Strategy.compile() # have this return dict of strategies, then get variables, then finalize the settings

class Settings:
    #! need to test this class out
    settings = {}
    
    def __init__(self, settings: Dict = {}):
        self.update(settings)

    # @classmethod
    # def from_dict(cls, settings: Dict) -> 'Settings':
    #     """ Create a settings object from a dictionary """
    #     return cls(**settings)
    
    def update(self, settings) -> 'Settings':
        """ Compile a settings object from a dictionary """
        self.settings['variables'] = self.update_variables(settings)
        self.settings['components'] = self.update_components(settings)
        
        
    def update_components(self, settings):
        """ Update component settings """
        final_components = {}
        for component, modules in _COMPONENTS.items():
            for module, functions in modules.items():
                for function in functions:
                    if function.name in settings:
                        final_components[function.name] = settings[function.name]
                    else:
                        final_components[function.name] = function.default
                        
        return final_components
    
    def update_variables(self, settings):
        #! double check this
        """ Update variable settings """
        variable_dict = Variables.compile()
        final_variables = {}
        for variables in variable_dict.values():
            for variable in variables:
                if variable.name in settings:
                    final_variables[variable.name] = settings[variable.name]
                else:
                    final_variables[variable.name] = variable.default
                    
        return final_variables
        
    
    def compile(self, name):
        #! clean up the Strategy class???
        strategies = Strategy.dict()
        pass
    
    def get(self, model: str) -> 'Settings':
        """ Get a setting """
        return self.settings[model]