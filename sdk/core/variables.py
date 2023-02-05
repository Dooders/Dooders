""" 
Variables
---------
This module contains the variables class for the SDK.
"""

import os
from typing import Dict

import yaml

from sdk.utils.types import Setting, Variable


class Variables:
    """ 
    Discover all variables for the applicable models
    """

    variables = {}

    @classmethod
    def discover(cls) -> Dict[str, list]:
        """ 
        Discover all setting options 

        """

        for file in os.listdir('sdk/variables'):
            if file.endswith('.yml'):
                with open('sdk/variables/' + file) as f:

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

        return cls.variables
