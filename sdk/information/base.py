from functools import partial
from typing import Callable, List

import pandas as pd
from pydantic import BaseModel


class BaseCollector(BaseModel):
    name: str
    function: Callable
    component: str


class BaseInformation:
    """ 
    """

    simulation = None

    def __init__(self, collectors: List[BaseCollector]) -> None:
        """ 
        Initialize the collector.

        Args:
            collectors: List of collectors to be used.
        """
        self.collectors: dict = {}
        self.data: dict = {}

        for collector in collectors:
            self._add_collector(collector)

    def _add_collector(self, collector: BaseCollector) -> None:
        """ 
        Add a collector to the collector dictionary.

        Args:
            collector: Collector to be added.
        """
        collector = BaseCollector(**collector)
        component = collector.component

        if component not in self.collectors:
            self.collectors[component] = {}
            self.data[component] = {}

        if type(collector.function) is str:
            func = partial(self._getattr, collector.function)
        else:
            func = collector.function

        self.collectors[component][collector.name] = func
        self.data[component][collector.name] = []

    def _reporter_decorator(self, reporter):
        return reporter()

    def _collect(self, component: str, simulation) -> None:
        """
        """
        for name, func in self.collectors[component].items():

            if callable(func):
                # func = self._reporter_decorator(func)
                self.data[component][name].append(func(simulation))
            else:

                if func[1] is None:
                    self.data[component][name].append(func[0](simulation))
                else:
                    self.data[component][name].append(
                        func[0](simulation, **func[1]))

    def collect(self, simulation):
        """Collect all the data for the given simulation object."""
        for component, collector in self.collectors.items():
            self._collect(component, simulation)

    @staticmethod
    def _getattr(name, _object):
        """Turn around arguments of getattr to make it partially callable."""
        return getattr(_object, name, None)

    def get_dataframe(self, component: str) -> pd.DataFrame:
        """
        """
        df = pd.DataFrame.from_dict(self.data[component], orient="columns")

        return df
