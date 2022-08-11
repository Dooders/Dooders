from mesa.datacollection import DataCollector
from pydantic import BaseModel

from dooders.data import ExperimentResults
from dooders.logger import get_logger


class AgentInformation(BaseModel):
    agent_id: int
    energy: int
    direction: str
    x: int
    y: int


class SimulationInformation(BaseModel):
    agent_count: int
    energy_count: int
    direction_counts: dict


class Information(DataCollector):

    def __init__(self, experiment_id, model_reporters: SimulationInformation = None, agent_reporters: AgentInformation = None, rollup_reporters: dict = None):
        """
        Create a new DataCollector object.

        Args:
            experiment_id: The unique ID of the experiment.
            model_reporters: A dictionary of model level reporters.
            agent_reporters: A dictionary of agent level reporters.
            rollup_reporters: A dictionary of rollup reporters.
        """
        super().__init__(model_reporters, agent_reporters)
        self.rollup_reporters = {}
        self.rollup_vars = {}
        self.logger = get_logger()
        self.granularity = 2
        self.experiment_id = experiment_id

        if rollup_reporters is not None:
            for name, reporter in rollup_reporters.items():
                self._new_rollup_reporter(name, reporter)

    def _new_rollup_reporter(self, name: str, reporter: callable) -> None:
        """
        Create a new rollup reporter.

        Args:
            name: The name of the reporter.
            reporter: The reporter function.
        """
        # ? do I need to add a check to see if the reporter is a function
        self.rollup_reporters[name] = reporter
        self.rollup_vars[name] = []

    def collect(self, simulation) -> None:
        """
        Collect data from the model.

        Args:
            simulation: The model to collect data from.
        """
        super().collect(simulation)

        # data rollup to model level
        # replicate how mesa does a function based data collection
        # ? can I make this from a decorator
        if self.rollup_reporters:
            for var, reporter in self.rollup_reporters.items():
                self.rollup_vars[var].append(
                    self._reporter_decorator(reporter))

    def get_result_dict(self) -> ExperimentResults:
        """
        Get a dictionary of the results of the experiment.

        Returns:
            A dictionary of the results of the experiment.
        """
        result_dict = dict()
        for var, reporter in self.rollup_reporters.items():
            result_dict[var] = self.rollup_vars[var]
        return result_dict

    def log(self, message: str, granularity: int) -> None:
        """
        Log a message.

        Args:
            message: The message to log.
            granularity: The granularity of the message.
        """
        if granularity <= self.granularity:  # enviroment variable???
            message_string = f"{self.experiment_id}  - {message}"
            self.logger.info(message_string)
