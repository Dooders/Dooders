""" 
Variables module
----------------
This module contains the Variables class, which is used to discover all
variables for the applicable models.

Variables are used to configure the simulation and models. The variables
class is used to compile the variables dictionary from a user-provided
dictionary. The variables dictionary is then used to configure the
simulation and models.

Variables will be set as a class attribute on the applicable model class.
"""

import os
from typing import Dict

import yaml

from sdk.utils.types import Setting, Variable


class Variables:
    """ 
    Discover all variables for the applicable models

    Methods
    -------
    discover()
        Discover all setting options
    """

    variables = {}

    @classmethod
    def discover(cls) -> Dict[str, list]:
        """ 
        Discover all variables 

        Returns:
            Dict[str, list]: A dictionary where the key is the file name 
            and the value is a list of Variable objects.
        """

        directory = 'sdk/variables'
        for file in os.listdir(directory):
            if file.endswith('.yml'):
                with open(os.path.join(directory, file)) as f:
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
