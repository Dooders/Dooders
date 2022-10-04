import pandas as pd
from sdk.core import Collector


#! Change this to an abstract class, with internal methods not needed in child class

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
        Collector.compile_collectors(self)

    def collect(self, simulation) -> None:
        """
        Collect data from the simulation.
        
        Args:
            simulation: The simulation to collect data from.
        """
        Collector.run_collectors(self, simulation)

    @staticmethod
    def _getattr(name, _object) -> object:
        """Turn around arguments of getattr to make it partially callable."""
        return getattr(_object, name, None)

    def get_dataframe(self, scope: str) -> pd.DataFrame:
        """
        Get the collected data as a pandas DataFrame.

        Args:
            scope: Scope to get data from.

        Returns:
            DataFrame of collected data.
        """
        data = self.data[scope]
        
        
        if scope == 'dooder':
            sub_data = data['Stat']
            data = [item for sublist in sub_data for item in sublist]
        
        df = pd.DataFrame.from_dict(data, orient="columns")

        return df
