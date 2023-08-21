""" 
InternalModels
--------------
The InternalModels class models a Dooder's learned behaviors.

How the internal models are created at simulation start:
...
"""

from dooders.sdk.core.default_settings import default_settings
from dooders.sdk.core.settings import Settings
from dooders.sdk.learning.scratch.model import SimpleNeuralNet

DEFAULT_SETTINGS = default_settings['internal_models']


class InternalModels(dict):
    """ 
    Works like a normal dictionary but with a method to easily replace
    the weights of the internal models.

    Each model is created when the class is instantiated. The models are
    stored as a dictionary with the model name as the key.

    Parameters
    ----------
    model_list : list
        A list of model names to use as keys for the dictionary.

    Methods
    -------
    build(model_list: list) -> None
        Build the internal models.
    inherit_weights(weights: dict) -> None
        Take a dictionary of weights and inherit them into the internal models.

    Properties
    ----------
    weights : dict
        Dictionary of weights from the internal models.
    biases : dict
        Biases from the internal models.
    """

    def __init__(self, id: str, model_dict: dict = DEFAULT_SETTINGS, *args, **kwargs) -> None:
        self.build(id, model_dict)
        super(InternalModels, self).__init__(*args, **kwargs)

    def build(self, id: str, model_dict: dict) -> None:
        """
        Build the internal models.

        Parameters
        ----------
        model_list : list
            A list of model names to use as keys for the dictionary.
        """
        for model_name in model_dict:
            instructions = model_dict[model_name]
            self[model_name] = SimpleNeuralNet(id, instructions)

    def inherit_weights(self, weights: dict) -> None:
        """ 
        Take a dictionary of weights and inherit them 
        into the internal models.

        Parameters
        ----------
        weights : dict
            A dictionary of weights to inherit.
        """
        for model in self.keys():
            self[model].inherit_weights(weights[model])

    def save(self, path: str) -> None:
        """ 
        Save the internal models to a directory.

        Parameters
        ----------
        path : str
            The path to the directory to save the models to.
        """
        for model in self.keys():
            self[model].save(f"{path}_{model}_weights")

    @property
    def weights(self) -> dict:
        """ 
        Dictionary of weights from the internal models.

        Returns
        -------
        model_weights : dict
            A dictionary of weights from the internal models.
        """
        model_weights = dict()

        for model in self.keys():
            model_weights[model] = self[model].weights

        return model_weights

    @property
    def biases(self) -> dict:
        """ 
        Biases from the internal models.

        Returns
        -------
        biases : dict
            A dictionary of biases from the internal models.
        """
        keys = self.keys()
        biases = dict()

        for key in keys:
            biases[key] = self[key].biases

        return biases
