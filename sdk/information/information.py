from typing import List
from sdk.data import ExperimentResults
from sdk.information.base import BaseInformation
from sdk.logger import get_logger


class Information(BaseInformation):

    def __init__(self, experiment_id):
        """
        Create a new DataCollector object.

        Args:
            experiment_id: The unique ID of the experiment.
        """
        super().__init__()
        self.logger = get_logger()
        self.granularity = 2
        self.experiment_id = experiment_id

    # def _new_rollup_reporter(self, name: str, reporter: callable) -> None:
    #     """
    #     Create a new rollup reporter.

    #     Args:
    #         name: The name of the reporter.
    #         reporter: The reporter function.
    #     """
    #     # ? do I need to add a check to see if the reporter is a function
    #     self.rollup_reporters[name] = reporter
    #     self.rollup_vars[name] = []

    def collect(self, simulation) -> None:
        """
        Collect data from the simulation.

        Args:
            simulation: The simulation to collect data from.
        """
        super().collect(simulation)

        # data rollup to simulation level
        # replicate how mesa does a function based data collection
        # ? can I make this from a decorator
        # if self.rollup_reporters:
        #     for var, reporter in self.rollup_reporters.items():
        #         self.rollup_vars[var].append(
        #             self._reporter_decorator(reporter))
                
        # print(self.get_result_dict(simulation))

    def get_result_dict(self, simulation) -> ExperimentResults:
        """
        Get a dictionary of the results of the experiment.

        Returns:
            A dictionary of the results of the experiment.
        """
        result_dict = dict()
        result_dict['CycleCount'] = simulation.time.time

        # iterate through the data collectors and add the data to the result dict
        for _, values in simulation.information.data.items():
            for column, value in values.items():
                result_dict[column] = value[-1] # get the last value
                
        return result_dict

    def log(self, message: str, granularity: int) -> None:
        """
        Log a message.

        Args:
            message: The message to log.
            granularity: The granularity of the message.
        """
        if granularity <= self.granularity:  # enviroment variable???
            message_string = f"'experiment_id':'{self.experiment_id}', {message}"
            self.logger.info(message_string)
            
            
    # function to read log json from the last record to the first record
    def read_log(self) :
        with open('logs/log.log', 'r') as f:
            for line in f:
                yield line
                
                
    def get_experiment_log(self, experiment_id: str = 'Current') -> List[str]:
        """
        Get the log for a given experiment.

        Args:
            experiment_id: The id of the experiment.
        """
        
        if experiment_id == 'Current':
            experiment_id = self.experiment_id

        for line in self.read_log():
            if experiment_id in line:
                yield line
                
    def get_object_history(self, object_id: str):
        for line in self.get_experiment_log():
            if object_id in line:
                return line