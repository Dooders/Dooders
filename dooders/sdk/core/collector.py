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

from typing import TYPE_CHECKING, Callable

from pydantic import BaseModel

from dooders.sdk.core.core import Core

if TYPE_CHECKING:
    from dooders.sdk.simulation import Simulation


class BaseCollector(BaseModel):
    function: Callable
    file_name: str
    function_name: str
    enabled: bool


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
        
    Methods
    -------
    _initialize_collectors()
        Compile the collectors into a dictionary.
    collect(simulation: Simulation) -> None
        Collects the data from the collectors.
    """

    def __init__(self) -> None:
        self.collectors = []
        self.data: dict = {}
        self._initialize_collectors()

    def _initialize_collectors(self) -> None:
        """ 
        Compile the collectors into a dictionary.
        
        Examples
        --------
        >>> from sdk.core.collector import Collector
        >>>
        >>> Collector.compile_collectors()
        """
        component = self.get_components('collector')

        for collectors in component.values():

            for collector in collectors.values():
                base_collector = BaseCollector(function_name=collector.function_name,
                                               function=collector.function,
                                               file_name=collector.file_name,
                                               enabled=collector.enabled)
                scope = base_collector.file_name

                if scope not in self.data:
                    self.data[scope] = {}
                self.data[scope][base_collector.function_name] = []
                
                self.collectors.append(base_collector)

    def collect(self, simulation: 'Simulation') -> None:
        """
        Run all the collectors for all the components.

        Parameters
        ----------
        simulation: Simulation
            Simulation object to collect data from.
        """
        for collector in self.collectors:
            name, data = collector.function(simulation)
            self.data[collector.file_name][name].append(data)