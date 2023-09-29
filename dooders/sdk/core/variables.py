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
from importlib import resources
from pathlib import Path
from typing import Dict

import yaml

from dooders.sdk.utils.types import Setting, Variable


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

        Returns
        -------
        variables : dict
            A dictionary of variables, where the key is the model name
            and the value is a list of variables.

        Examples
        --------
        >>> from sdk.core.variables import Variables
        >>> variables = Variables.discover()
        >>> variables
        {'model': [<sdk.utils.types.Variable object at 0x7f8b8c0b0a90>]}
        """
        dir_path = resources.files("dooders.sdk") / "variables"

        for file in dir_path.iterdir():
            if file.suffix == ".yml":
                with open(os.path.join(dir_path, file)) as f:
                    options = yaml.load(f, Loader=yaml.FullLoader)
                    option_list = []

                    for name, option in options.items():
                        default = Setting(
                            function=option["function"], args=option["args"]
                        )
                        variable = Variable(name=name, default=default, **option)

                        option_list.append(variable)
                variable_name = str(file).split("/")[-1].split(".")[0]
                cls.variables[variable_name] = option_list

        return cls.variables
