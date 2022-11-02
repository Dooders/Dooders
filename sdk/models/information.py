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

import ast
from typing import TYPE_CHECKING, List

from db.main import DB
from sdk.base.base_information import BaseInformation
from sdk.utils.logger import get_logger

if TYPE_CHECKING:
    from sdk.core.data import UniqueID
    from sdk.simulation import Simulation


#! Add post_collect process to send results to db
#! Have collectors stored in Collectors class
#! Have a better way to run functions, scope by scope, with correct args

class Information(BaseInformation):
    """
    Class for collecting data from the simulation.
    """

    def __init__(self, simulation: 'Simulation') -> None:
        """
        Create a new Information component.

        Args:
            simulation_id: The unique ID of the experiment.
            params: The parameters of the experiment.

        Attributes:
            simulation_id: The unique ID of the experiment.
            logger: The logger for the experiment.
            granularity: The granularity of the experiment.
        """
        super().__init__()
        self.logger = get_logger()
        self.granularity = 2  # ! Fix this
        self.simulation = simulation
        self.simulation_id = simulation.simulation_id

    def collect(self, simulation: 'Simulation') -> None:
        """
        Collect data from the simulation.

        Args:
            simulation: The simulation to collect data from.
        """
        super().collect(simulation)
        self.post_collect()

    def post_collect(self) -> None:
        cycle_results = self.get_result_dict(self.simulation)['simulation']
        cycle_results['ID'] = self.simulation.generate_id()
        
        if self.simulation.send_to_db:
            DB.add_record(cycle_results, 'CycleResults')

    def get_result_dict(self, simulation: 'Simulation') -> dict:
        """
        Get a dictionary of the results of the experiment.

        Args:
            simulation: The simulation to collect data from.

        Returns:
            A dictionary of the results of the experiment.
        """
        result_dict = dict()

        for scope, values in self.data.items():
            result_dict[scope] = {}
            result_dict[scope]['CycleNumber'] = simulation.time.time
            result_dict[scope]['SimulationID'] = self.simulation_id
            for column, value in values.items():
                result_dict[scope][column] = value[-1]  # get the last value

        return result_dict

    def log(self, message: str, granularity: int) -> None:
        """
        Log a message.

        Args:
            message: The message to log.
            granularity: The granularity of the message.
        """
        if granularity <= self.granularity:  # environment variable???
            message_string = f"'SimulationID':'{self.simulation_id}', {message}"
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

    def get_experiment_log(self, simulation_id: 'UniqueID' = 'Current') -> List[str]:
        """
        Get the log for a given experiment.

        Args:
            simulation_id: The id of the experiment.

        Yields:
            A list of the lines in the log file.
        """

        if simulation_id == 'Current':
            simulation_id = self.simulation_id

        for line in self.read_log():
            if simulation_id in line:
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

    def get_log(self) -> List[dict]:
        logs = []
        with open(f"logs/log.log", "r") as f:
            lines = f.readlines()
            for line in lines:
                if self.simulation_id in line:
                    final = line[:-2]
                    logs.append(ast.literal_eval(final))

        return logs
