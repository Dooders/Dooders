""" 
Settings
--------
This module contains the settings class for the SDK.
"""

from typing import Dict

from sdk.core import Strategy
from sdk.core.variables import Variables

# no need to store instance of this anymore
# Strategy.compile() # have this return dict of strategies, then get variables, then finalize the settings

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
        #! double check this
        variable_dict = Variables.compile()
        for variables in variable_dict.values():
            for variable in variables:
                if variable.name in settings:
                    self.settings[variable.name] = settings[variable.name]
                else:
                    self.settings[variable.name] = variable.default
    
    def compile(self, name):
        #! clean up the Strategy class???
        strategies = Strategy.dict()
        pass
    
    def get(self, model: str) -> 'Settings':
        """ Get a setting """
        return self.settings[model]