"""
Information component used to collect information from the simulation.
This class provides the prim ary capability to collect information from the
simulation at the end of each cycle. The information is stored in a dictionary
named 'data'.

Collectors are the registered functions that are used to collect specific data.
All collectors are stored in the collectors attribute. The collectors attribute
is a dictionary of dictionaries. The first key is the collector component.

This component is also the main method to log activity from the simulation.
All activity is logged to a file based on specified granularity. Granularity
is defined as the level of detail to log. 1 is the lowest and most important
level of detail. 3 is the highest and most detailed level of detail, including
when energy dissipation occurs, failed movements, and failed actions, etc..
"""

from typing import List

from sdk.base.base_information import BaseInformation
from sdk.logger import get_logger


class Information(BaseInformation):
    """
    Class for collecting data from the simulation.
    """

    def __init__(self, experiment_id: str, params: dict) -> None:
        """
        Create a new Information component.

        Args:
            experiment_id: The unique ID of the experiment.
            params: The parameters of the experiment.

        Attributes:
            experiment_id: The unique ID of the experiment.
            logger: The logger for the experiment.
            granularity: The granularity of the experiment.
        """
        super().__init__()
        self.logger = get_logger()
        self.granularity = params.Granularity
        self.experiment_id = experiment_id

    def collect(self, simulation) -> None:
        """
        Collect data from the simulation.

        Args:
            simulation: The simulation to collect data from.
        """
        super().collect(simulation)
        
        # TODO: Will add post collect rollups here

    def get_result_dict(self, simulation) -> dict:
        """
        Get a dictionary of the results of the experiment.

        Args:
            simulation: The simulation to collect data from.

        Returns:
            A dictionary of the results of the experiment.
        """
        result_dict = dict()
        result_dict['CycleCount'] = simulation.time.time

        for _, values in self.data.items():
            for column, value in values.items():
                result_dict[column] = value[-1]  # get the last value

        return result_dict

    def log(self, message: str, granularity: int) -> None:
        """
        Log a message.

        Args:
            message: The message to log.
            granularity: The granularity of the message.
        """
        if granularity <= self.granularity:  # environment variable???
            message_string = f"'experiment_id':'{self.experiment_id}', {message}"
            self.logger.info(message_string)

    def read_log(self) -> List[str]:
        """
        Read the log file.

        Yields:
            A list of the lines in the log file.
        """
        with open('logs/log.log', 'r') as f:
            for line in f:
                yield line

    def get_experiment_log(self, experiment_id: str = 'Current') -> List[str]:
        """
        Get the log for a given experiment.

        Args:
            experiment_id: The id of the experiment.

        Yields:
            A list of the lines in the log file.
        """

        if experiment_id == 'Current':
            experiment_id = self.experiment_id

        for line in self.read_log():
            if experiment_id in line:
                yield line

    def get_object_history(self, object_id: str) -> List[str]:
        """
        Get the history of an object.

        Args:
            object_id: The id of the object. 

        Returns:
            A list of the lines in the log file.
        """
        for line in self.get_experiment_log():
            if object_id in line:
                print(line)