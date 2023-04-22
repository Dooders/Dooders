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

from dooders.sdk.core import Collector
from dooders.sdk.utils.logger import get_logger

if TYPE_CHECKING:
    from dooders.sdk.simulation import Simulation
    
    
class FakeLogger:
    
    def info(self, message: str) -> None:
        pass
    def log(self, message: str, granularity: int) -> None:
        pass


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

    @classmethod
    def _init_information(cls, simulation: 'Simulation') -> None:
        cls.collectors = Collector()
        cls.logger = FakeLogger()
        cls.granularity = 2
        cls.simulation_id = simulation.simulation_id

    @classmethod
    def collect(cls, simulation: 'Simulation') -> None:
        """
        Collect data from the simulation.

        Parameters
        ----------
        simulation: Object
            Data is collected from the simulation object.
        """
        cls.collectors.collect(simulation)

    @classmethod
    def log(cls, message: str, granularity: int) -> None:
        """
        Log a message.

        Parameters
        ----------
        message: str
            The message to log.
        granularity: int
            The granularity of the message.
        """
        if granularity <= cls.granularity:
            message_string = f"'SimulationID':'{cls.simulation_id}', {message}"

            cls.logger.info(message_string) 

    @classmethod
    @property
    def data(cls) -> dict:
        """ 
        Get the data collected from the simulation.

        Returns
        -------
        data: dict
            A dictionary of the data collected from the simulation.
        """
        return cls.collectors.data
