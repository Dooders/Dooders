"""
Information Model
-----------------
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

import pandas as pd

from db.main import DB
from sdk.core import Collector
from sdk.utils.logger import get_logger

if TYPE_CHECKING:
    from sdk.core.data import UniqueID
    from sdk.simulation import Simulation


class Information:
    """
    Class for collecting data from the simulation.

    Parameters
    ----------
    simulation_id: str
        The unique ID for the simulation.

    Attributes
    ----------
    simulation_id: see Parameters
    logger: Logger
        Logger that handles all logging for the simulation.
    granularity: int
        Higher granularity means more detailed logging.
        
    Methods
    -------
    collect(simulation: 'Simulation')
        Collect data from the simulation.
    post_collect()
        Process taking place after data collection.
    get_result_dict(simulation: 'Simulation')
        Get a dictionary of the results of the experiment.
    """

    def __init__(self, simulation: 'Simulation') -> None:
        self.collectors = Collector()
        self.logger = get_logger()
        self.granularity = 2
        self.simulation = simulation
        self.simulation_id = simulation.simulation_id

    def collect(self, simulation: 'Simulation') -> None:
        """
        Collect data from the simulation.

        Parameters
        ----------
        simulation: Object
            Data is collected from the simulation object.
        """
        self.collectors.collect(simulation)
        self.post_collect()

    def post_collect(self) -> None:
        """ 
        Process taking place after data collection.

        Like aggregating data and sending to a database.
        """
        # cycle_results = self.get_result_dict(self.simulation)['simulation']
        # cycle_results['ID'] = self.simulation.generate_id()

        # if self.simulation.send_to_db:
        #     DB.add_record(cycle_results, 'CycleResults')

    def get_result_dict(self, simulation: 'Simulation') -> dict:
        """
        Get a dictionary of the results of the experiment.

        Parameters
        ----------
        simulation: 
            To extract the results from the simulation.

        Returns
        -------
        result_dict: dict
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

    def get_dataframe(self, scope: str) -> pd.DataFrame:
        """
        Get the collected data as a pandas DataFrame.

        Parameters
        ----------
        scope: str
            Scope to get data from.

        Returns:
        df: pd.DataFrame
            DataFrame of collected data.
        """
        data = self.collectors.data[scope]

        if scope == 'dooder':
            sub_data = data['Stat']
            data = [item for sublist in sub_data for item in sublist]

        df = pd.DataFrame.from_dict(data, orient="columns")

        return df

    def log(self, message: str, granularity: int) -> None:
        """
        Log a message.

        Parameters
        ----------
        message: str
            The message to log.
        granularity: int
            The granularity of the message.
        """
        if granularity <= self.granularity:
            message_string = f"'SimulationID':'{self.simulation_id}', {message}"
            
            # disabled for now:
            # self.logger.info(message_string) 

    def read_log(self) -> str:
        """
        Read the log file.

        Yields
        ------
        line: str
            A line in the log file.
        """
        with open('logs/log.json', 'r') as f:
            for line in f:
                yield line

    #! add log methods to log class
    def get_experiment_log(self, simulation_id: 'UniqueID' = 'Current') -> str:
        """
        Get the log for a given experiment.

        Parameters
        ----------
        simulation_id: str

        Yields
        ------
        line: str
            A line in the logs of the current experiment.
        """

        if simulation_id == 'Current':
            simulation_id = self.simulation_id

        for line in self.read_log():
            if simulation_id in line:
                yield line

    def get_object_history(self, object_id: str) -> None:
        """
        Print the history of an object.

        Parameters
        ----------
        object_id: str
            The id of the object. 
        """
        for line in self.get_experiment_log():
            if object_id in line:
                print(line)

    def get_log(self) -> List[dict]:
        """ 
        Get the log for the current experiment.

        Returns
        -------
        logs: List[dict]
            A list of dictionaries containing the log for the current experiment.
        """
        logs = []
        with open(f"logs/log.json", "r") as f:
            lines = f.readlines()
            for line in lines:
                if self.simulation_id in line:
                    final = line[:-2]
                    logs.append(ast.literal_eval(final))

        return logs

    @property
    def data(self) -> dict:
        """ 
        Get the data collected from the simulation.

        Returns
        -------
        data: dict
            A dictionary of the data collected from the simulation.
        """
        return self.collectors.data
