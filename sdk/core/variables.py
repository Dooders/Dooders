
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

class Variables:
    
    variables = {}
    
    @classmethod
    def discover(cls) -> None:
        """ Discover all setting options """

        for file in os.listdir('sdk/settings'):
            if file.endswith('.yml'):
                with open('sdk/settings/' + file) as f:
                    
                    options = yaml.load(f, Loader=yaml.FullLoader)
                    option_list = []
                    for name, option in options.items():
                        default = Setting(**option)
                        variable = Variable(name=name, 
                                            type=option['type'], 
                                            default=default)
                        option_list.append(variable)
                cls.variables[file.split('.')[0]] = option_list