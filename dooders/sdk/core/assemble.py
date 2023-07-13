# """
# Simulation Assemble
# -------------------
# This module is used to assemble the simulation. It is used to import all the
# necessary modules and classes to run the simulation.
# """

import importlib
from typing import List

from dooders.sdk.config import Config
from dooders.sdk.core import (Action, Condition, Policy, Settings, Strategy,
                              Surface)
from dooders.sdk.models.environment import Environment
from dooders.sdk.simulation import Simulation

#! need to simplify settings
#! need easy way to "discover" existing settings

class Assemble:
    """
    Assemble the simulation by importing necessary modules and classes.

    Methods
    -------
    execute()
        Execute the assembly of the simulation.

    Attributes
    ----------  
    BASE_MODELS: List[str]
        A list of strings representing the base models.
    ALL_MODELS: List[str]
        A list of strings representing all the models.
    """

    BASE_MODELS: List[str] = ['environment']
    ALL_MODELS: List[str] = BASE_MODELS + ['resources', 'arena']

    @classmethod
    def execute(cls, user_settings: dict = {}) -> Simulation:
        """
        Execute the assembly of the simulation.

        Returns
        -------
        simulation: Simulation
            A `Simulation` object representing the simulation.

        """
        #! need to improve the dynamic variable creation
        settings_old = Settings.compile()
        final_settings = Config(user_settings)

        simulation = Simulation(final_settings)

        for model_name in cls.ALL_MODELS:
            try:
                module = importlib.import_module(
                    f'dooders.sdk.models.{model_name}')
            except ImportError:
                raise ImportError(
                    f"Failed to import module for model '{model_name}'")

            class_name = model_name.title()
            model_class = getattr(module, class_name)
            model = model_class(simulation, final_settings)
            model_variables = settings_old['variables'][model_name]
            Strategy.compile(model, model_variables)
            cls._setup_model(simulation, model_name, model)
            
        simulation.setup()

        return simulation

    @staticmethod
    def _setup_model(simulation: Simulation, model_name: str, model: object) -> None:
        """
        Set up a model in the simulation.

        Parameters
        ----------
        simulation: Simulation
            A `Simulation` object representing the simulation.
        model_name: str
            A string representing the name of the model.
        model: object
            An object representing the model.

        """
        setattr(simulation, model_name, model)
        model._setup()
