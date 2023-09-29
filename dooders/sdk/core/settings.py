""" 
Core: Settings
--------------
This module contains the settings class for the SDK.

Settings are used to configure the simulation and models. The settings
class is used to compile the settings dictionary from a user-provided
dictionary. The settings dictionary is then used to configure the
simulation and models.
"""

from dooders.sdk.core.core import _COMPONENTS
from dooders.sdk.core.default_settings import default_settings
from dooders.sdk.core.variables import Variables

DEFAULT_SETTINGS = default_settings


class Settings:
    """
    Settings class to update defaults, if provided by the user.

    On initialization, the settings dictionary is updated with the
    user-provided settings. The settings dictionary is then used to
    configure the simulation and models.

    Attributes
    ----------
    settings : dict
        The settings dictionary used to assemble the simulation.

    Methods
    -------
    compile(settings: dict = {}) -> dict
        Compile a settings object from a dictionary.
    update_components(settings: dict) -> dict
        Update component settings.
    update_variables(settings: dict) -> dict
        Update variable settings based on user input.
    get(type: str, model: str, variable: str) -> Any
        Get a variable from the settings dictionary.
    """

    settings: dict = {}

    @classmethod
    def compile(cls, settings: dict = {}) -> dict:
        """
        Compile a settings object from a dictionary

        Parameters
        ----------
        settings : dict
            The settings dictionary to update, provided by the user.

        Returns
        -------
        cls.settings : dict
            The updated settings dictionary.

        Examples
        --------
        >>> from sdk.core.settings import Settings
        >>>
        >>> Settings.compile({'max_steps': 100})
        """
        cls.settings["variables"] = cls.update_variables(settings)
        cls.settings["components"] = cls.update_components(settings)

        return cls.settings

    @classmethod
    def update_components(cls, settings: dict) -> dict:
        """
        Update component settings

        Parameters
        ----------
        settings : dict
            The settings dictionary to update, provided by the user.

        Returns
        -------
        final_components : dict
            The updated settings dictionary for all components.

        Examples
        --------
        >>> from sdk.core.settings import Settings
        >>>
        >>> Settings.update_components({'simulation': 'sdk.simulations'})
        """
        final_components = {}
        for component, modules in _COMPONENTS.items():
            for module, functions in modules.items():
                for function in functions:
                    if function in settings:
                        final_components[function] = settings[function]
                    else:
                        final_components[function] = function

        return final_components

    @classmethod
    def update_variables(cls, settings: dict) -> dict:
        """
        Update variable settings based on user input.

        If a setting is not provided, the default option will be used.

        Parameters
        ----------
        settings : dict
            The settings dictionary to update, provided by the user.

        Returns
        -------
        final_settings : dict
            The updated settings dictionary for all model variables.

        Examples
        --------
        >>> from sdk.core.settings import Settings
        >>>
        >>> Settings.update_variables({'max_steps': 100})
        """
        variable_dict = Variables.discover()
        final_settings = {}
        for model, variables in variable_dict.items():
            model_settings = {}
            for variable in variables:
                model_settings[variable.name] = settings.get(
                    variable.name, variable.default
                )
            final_settings[model] = model_settings

        return final_settings

    @classmethod
    def get(cls, type: str, model: str = None) -> dict:
        """
        Get settings for a given model.

        Parameters
        ----------
        type : str
            The type of settings to return. Options are 'variables' or
            'components'.
        model : str, optional
            The model to return settings for. If no model is provided, the
            settings for all models will be returned.

        Returns
        -------
        settings : dict
            The settings for the given model.

        Examples
        --------
        >>> from sdk.core.settings import Settings
        >>>
        >>> Settings.get('variables', 'simulation')
        """
        if model is None:
            return cls.settings[type]
        else:
            return cls.settings[type][model]

    @classmethod
    def search(cls, setting_name: str) -> str:
        """
        Search for a specific setting.

        Parameters
        ----------
        setting_name : str
            The name of the policy to search for.

        Returns
        -------
        setting : str
            The name of the policy that matches the search term.

        Examples
        --------
        >>> from sdk.core.settings import Settings
        >>>
        >>> Settings.search('Movement')
        "NeuralNetwork"
        """
        for setting in cls.settings["variables"].values():
            if setting_name in setting.keys():
                return setting[setting_name].args["value"]
