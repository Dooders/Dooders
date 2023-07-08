import json

from dooders.data.dooder_dataframe import get_dooder_df
from dooders.data.gene_embedding_dataframe import get_gene_embedding_df
from dooders.data.inference_record_dataframe import get_inference_record_df
from dooders.data.experiment_results import (calculate_accuracies,
                                        decision_analysis, near_hunger,
                                        probabilities, stuck_streak_counts)


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
        Run through the data transformation steps
        """
        self.hunger_analysis()
        self.probability_analysis()
        self.accuracy_analysis()
        self.decision_analysis()

    def accuracy_analysis(self) -> None:
        """ 
        Calculates the accuracy column

        Creates the following columns:
        - accuracy
        """
        accuracies = calculate_accuracies(self.inference_df)
        self.dooder_df['accuracy'] = self.dooder_df['id'].map(accuracies)

    def probability_analysis(self) -> None:
        """ 
        Calculates the starting success probability column

        Creates the following columns:
        - starting_success_probability
        """
        probability_dict = probabilities(self.inference_df)
        self.dooder_df['starting_success_probability'] = self.dooder_df['id'].map(
            probability_dict)

    def hunger_analysis(self) -> None:
        """ 
        Calculates the near death count and near death rate columns

        Creates the following columns:
        - near_death_count
        - near_death_rate
        """
        near_hunger_counts = near_hunger(self.inference_df)
        self.dooder_df['near_death_count'] = self.dooder_df['id'].map(
            near_hunger_counts)
        self.dooder_df['near_death_rate'] = self.dooder_df['near_death_count'] / \
            self.dooder_df['age']

    def decision_analysis(self) -> None:
        """ 
        Analyzes the decision making of the dooders

        Creates the following columns:
        - longest_stuck_length
        - minimum_percent_stuck
        - stuck_streak_count
        - was_stuck
        - ended_stuck
        """
        decision_counts = decision_analysis(self.inference_df)
        self.dooder_df['longest_stuck_length'] = self.dooder_df['id'].map(
            decision_counts)
        self.dooder_df['minimum_percent_stuck'] = self.dooder_df['longest_stuck_length'] / \
            self.dooder_df['age']

        # stuck streak analysis
        stuck_streaks = stuck_streak_counts(self.inference_df)
        self.dooder_df['stuck_streak_count'] = self.dooder_df['id'].map(
            stuck_streaks)
        self.dooder_df['was_stuck'] = self.dooder_df['longest_stuck_length'] >= 5
        self.dooder_df['ended_stuck'] = self.dooder_df['stuck_streak_count'] >= 5
