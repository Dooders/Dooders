""" 
Collector Core
--------------
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
from typing import TYPE_CHECKING, Callable

from pydantic import BaseModel

from sdk.base.base_core import BaseCore

if TYPE_CHECKING:
    from sdk.simulation import Simulation


class BaseCollector(BaseModel):
    name: str
    function: Callable
    scope: str


class Collector(BaseCore):
    """ 
    The factory class for creating collectors

    The CollectorRegistry is a global registry of collectors. A new collector
    is added through the register decorator.

    Attributes
    ----------
    registry: list
        List of all the registered collectors. Inside the collectors folder.
    collectors: dict
        Dictionary of all the collectors. The key is the collector name.
    data: dict
        Dictionary of all the collected data. The key is the collector name.
    """

    registry: list = []

    def __init__(self) -> None:
        self.collectors: dict = {}
        self.data: dict = {}
        self.compile_collectors()

    @classmethod
    def register(cls, name: str) -> Callable:
        """ 
        Register a collector in the registry.

        Parameters
        ----------
        name: str
            Name of the collector.

        Returns
        -------
        inner_wrapper: Callable
            The decorator function.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            scope = cls.infer_scope(cls, wrapped_class)
            cls.registry.append(
                {'name': name, 'function': wrapped_class, 'scope': scope})
            return wrapped_class

        return inner_wrapper

    def compile_collectors(self) -> None:
        """ 
        Compile the collectors into a dictionary.
        """
        for collector in self.registry:
            collector = BaseCollector(**collector)
            scope = collector.scope

            if scope not in self.collectors:
                self.collectors[scope] = {}
                self.data[scope] = {}

            if type(collector.function) is str:
                func = partial(self._getattr, collector.function)
            else:
                func = collector.function

            self.collectors[scope][collector.name] = func
            self.data[scope][collector.name] = []

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
