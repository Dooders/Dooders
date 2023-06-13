import json

from dooders.data.dooder_dataframe import get_dooder_df
from dooders.data.gene_embedding_dataframe import get_gene_embedding_df
from dooders.data.inference_record_dataframe import get_inference_record_df
from dooders.experiment_results import (calculate_accuracies, near_hunger,
                                        probabilities)


class ExperimentData:
    """ 
    Class to hold the data from an experiment

    Attributes
    ----------
    json_data : dict
        The json data from the experiment
    embedding_df : pandas.DataFrame
        The gene embedding dataframe
    dooder_df : pandas.DataFrame
        The dooder dataframe
    inference_df : pandas.DataFrame
        The inference record dataframe
    """

    def __init__(self, experiment_name: str):
        self.json_data = self._load_data(experiment_name)
        self.embedding_df = get_gene_embedding_df(self.json_data)
        self.dooder_df = get_dooder_df(self.json_data)
        self.inference_df = get_inference_record_df(self.json_data)
        self._transform()

    def _load_data(self, experiment_name: str) -> dict:
        """ 
        Loads the experiment data from the json file

        Parameters
        ----------
        experiment_name : str
            The name of the experiment to load the data from

        Returns
        -------
        dict
            The json data from the experiment
        """
        file_path = f'experiments/{experiment_name}/experiment_results.json'

        with open(file_path, "r") as f:
            json_data = json.load(f)

        return json_data

    def _transform(self) -> None:
        """ 
        Post initialization transformation of the data
        """
        near_hunger_counts = near_hunger(self.inference_df)
        self.dooder_df['near_death_count'] = self.dooder_df['id'].map(
            near_hunger_counts)
        self.dooder_df['near_death_rate'] = self.dooder_df['near_death_count'] / \
            self.dooder_df['age']

        probs = probabilities(self.inference_df)
        self.dooder_df['starting_success_probability'] = self.dooder_df['id'].map(
            probs)

        accuracies = calculate_accuracies(self.inference_df)
        self.dooder_df['accuracy'] = self.dooder_df['id'].map(accuracies)
