import json

import pandas as pd


class Investigate:
    """ 
    A class for investigating the results of an experiment.

    Attributes
    ----------
    experiment_name : str
        The name of the experiment.
    state : dict
        The state of the experiment.
    log : pd.DataFrame
        The log of the experiment.
    data : dict
        The information about the experiment.

    Methods
    -------
    load_log(file_path)
        Loads the contents of a JSON file into a Pandas DataFrame.
    load_state(folder_path, file_name)
        Loads the contents of a JSON file into a dictionary.
    """

    def __init__(self, experiment_name: str) -> None:
        self.experiment_name = experiment_name
        self.state = self.load_state(
            "experiments/" + experiment_name, "state.json")
        self.log = self.load_log(
            "experiments/" + experiment_name + "/log.json")
        self.data = self.state['information']

    def load_log(self, file_path: str) -> pd.DataFrame:
        """ 
        Loads the contents of a JSON file into a Pandas DataFrame.

        Parameters
        ----------
        file_path : str
            The path to the JSON file.

        Returns
        -------
        df : pd.DataFrame
            The contents of the JSON file as a Pandas DataFrame.
        """
        with open(file_path, 'r') as f:
            lines = [eval(line.strip())[0] for line in f]

        df = pd.DataFrame(lines)

        return df

    def load_state(self, folder_path: str, file_name: str) -> dict:
        """ 
        Loads the contents of a JSON file into a dictionary.

        Parameters
        ----------
        folder_path : str
            The path to the folder containing the JSON file.
        file_name : str
            The name of the JSON file.

        Returns
        -------
        json_data : dict
            The contents of the JSON file as a dictionary.
        """
        # Construct the full path to the JSON file
        file_path = folder_path + "/" + file_name

        # Open the file and read its contents
        with open(file_path, "r") as f:
            json_data = json.load(f)

        # Return the contents as a dictionary
        return json_data
