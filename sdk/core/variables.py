
import os
from typing import Union

import yaml
from pydantic import BaseModel

""" 
Variables
---------
This module contains the variables class for the SDK.
"""

from sdk.core.settings import Setting


class Variable(BaseModel):
    name: str
    type: str
    description: Union[str, None]
    default: Setting
    dependency: Union[str, None]


class Variables:

    variables = {}
      
    @classmethod  
    def list(cls, name=None) -> None:
        """ List all variables """
        cls.discover()
        if name:
            return cls.variables[name]
        else:
            return cls.variables

    @classmethod
    def discover(cls) -> None:
        """ Discover all setting options """

        for file in os.listdir('sdk/settings'):
            if file.endswith('.yml'):
                with open('sdk/settings/' + file) as f:

                    options = yaml.load(f, Loader=yaml.FullLoader)
                    option_list = []
                    for name, option in options.items():
                        default = Setting(function=option['function'],
                                          args=option['args'])
                        variable = Variable(name=name,
                                            default=default,
                                            **option)

                        option_list.append(variable)
                cls.variables[file.split('.')[0]] = option_list
