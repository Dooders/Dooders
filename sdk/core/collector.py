""" 
Core: Collector
---------------
The Collector class is a global registry of collectors. A new collector
is added through the register_collector() decorator. 

The decorator takes the name of the collector and component as arguments. The
component indicates what component or module the collector belongs to. The 
collector name is used to identify the collector in the output.

A collector serves as a method to extract information from the simulation 
at the end of each cycle. The information is stored in a dictionary, which 
is then passed to the Information component.

A collector can return any type of information. Every Collector must input 
'simulation' as an argument. The simulation object is used to extract 
information from the simulation.
"""

from functools import partial
from typing import TYPE_CHECKING, Callable, Dict, Union

from pydantic import BaseModel

from sdk.core.core import Core

if TYPE_CHECKING:
    from sdk.simulation import Simulation


class BaseCollector(BaseModel):
    function: Callable
    file_name: str
    function_name: str
    enabled: bool


CollectorDict: Dict[str, BaseCollector]
CollectorData: Dict[str, Union[list, dict, str, int, float]]


class Collector(Core):
    """ 
    The factory class for creating collectors

    The CollectorRegistry is a global registry of collectors. A new collector
    is added through the register decorator.

    Attributes
    ----------
    collectors: dict
        Dictionary of all the collectors. The key is the collector name.
    data: dict
        Dictionary of all the collected data. The key is the collector name.
    """

    def __init__(self) -> None:
        self.collectors: dict = {}
        self.data: dict = {}
        self.compile_collectors()

    def compile_collectors(self) -> None:
        """ 
        Compile the collectors into a dictionary.
        """
        #! change to a generator?
        component = self.get_components('sdk.collectors')

        for collectors in component.values():
            for collector in collectors.values():
                base_collector = BaseCollector(function_name=collector.function_name,
                                               function=collector.function,
                                               file_name=collector.file_name,
                                               enabled=collector.enabled)
                scope = base_collector.file_name

                if base_collector.enabled:

                    if scope not in self.collectors:
                        self.collectors[scope] = {}
                        self.data[scope] = {}

                    if type(base_collector.function) is str:
                        function = partial(self._getattr, collector.function)
                    else:
                        function = base_collector.function

                    self.collectors[scope][base_collector.function_name] = function
                    self.data[scope][base_collector.function_name] = []

    def collect(self, simulation: 'Simulation') -> None:
        """ 
        Run all the collectors for all the components.

        Parameters
        ----------
        simulation: Simulation
        Simulation object to collect data from.
        """
        for scope in self.collectors:
            self._collect(scope, simulation)

    def _collect(self, scope: str, simulation: 'Simulation') -> None:
        """
        Run all the collectors for the given component.

        Parameters
        ----------
        component: str
            Component to collect data from.
        simulation: Simulation
            Simulation object to collect data from.
        """
        for name, func in self.collectors[scope].items():

            if callable(func):
                self.data[scope][name].append(func(simulation))
            else:

                if func[1] is None:
                    self.data[scope][name].append(
                        func[0](simulation))
                else:
                    self.data[scope][name].append(
                        func[0](simulation, **func[1]))
