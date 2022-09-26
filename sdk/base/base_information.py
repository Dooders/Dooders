from functools import partial
from typing import Callable, List

import pandas as pd
from pydantic import BaseModel
from sdk.information.collectors import Collectors


class BaseCollector(BaseModel):
    name: str
    function: Callable
    component: str


class BaseInformation:
    """ 
    """

    simulation = None

    def __init__(self) -> None:
        """ 
        Initialize the collector.

        Args:
            collectors: List of collectors to be used.

        Attributes:
            collectors: Dictionary of collectors.
            data: Dictionary of data collected.
        """
        self.collectors: dict = {}
        self.data: dict = {}
        Collectors.compile_collectors(self)


    def _reporter_decorator(self, reporter):
        return reporter()

    def collect(self, simulation) -> None:
        """
        Collect all the data for the given simulation object.

        Args:
            simulation: Simulation object to collect data from.
        """
        for component, collector in self.collectors.items():
            Collectors.run_collectors(self, component, simulation)

    @staticmethod
    def _getattr(name, _object) -> object:
        """Turn around arguments of getattr to make it partially callable."""
        return getattr(_object, name, None)

    def get_dataframe(self, component: str) -> pd.DataFrame:
        """
        Get the collected data as a pandas DataFrame.

        Args:
            component: Component to get data from.

        Returns:
            DataFrame of collected data.
        """
        df = pd.DataFrame.from_dict(self.data[component], orient="columns")

        return df
