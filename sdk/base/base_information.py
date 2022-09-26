import pandas as pd
from sdk.information.collectors import Collectors


class BaseInformation:
    """ 
    """

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

    def collect(self, simulation) -> None:
        """
        Collect data from the simulation.
        
        Args:
            simulation: The simulation to collect data from.
        """
        Collectors.run_collectors(self, simulation)

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
