""" 
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
from statistics import mean
from typing import TYPE_CHECKING, Callable

from pydantic import BaseModel
from sdk.base.base_core import BaseCore

if TYPE_CHECKING:
    from sdk.information import Information
    from sdk.simulation import Simulation


class BaseCollector(BaseModel):
    name: str
    function: Callable
    scope: str


class Collector(BaseCore):
    """ 
    The factory class for creating collectors

    The CollectorRegistry is a global registry of collectors. A new collector
    is added through the register_collector() decorator.
    """

    # The registry of collectors
    registry = []

    @classmethod
    def register(cls, name: str) -> Callable:
        """ 
        Register a collector in the registry.

        Args:
            name: Name of the collector.
            scope: Scope of the collector.

        Returns:
            The decorator function.
        """

        def inner_wrapper(wrapped_class: Callable) -> Callable:
            scope = cls.infer_scope(cls, wrapped_class)
            cls.registry.append(
                {'name': name, 'function': wrapped_class, 'scope': scope})
            return wrapped_class

        return inner_wrapper

    @classmethod
    def compile_collectors(cls, information: 'Information') -> None:
        """ 
        Compile the collectors into a dictionary.

        Args:
            information: Information object to collect data from.
        """
        for collector in cls.registry:
            collector = BaseCollector(**collector)
            scope = collector.scope

            if scope not in information.collectors:
                information.collectors[scope] = {}
                information.data[scope] = {}

            if type(collector.function) is str:
                func = partial(information._getattr, collector.function)
            else:
                func = collector.function

            information.collectors[scope][collector.name] = func
            information.data[scope][collector.name] = []

    @classmethod
    def run_collectors(cls, information: 'Information', simulation: 'Simulation') -> None:
        """ 
        Run all the collectors for all the components.

        Args:
            information: Information object to collect data from.
            simulation: Simulation object to collect data from.
        """
        for scope in information.collectors:
            cls._collect(information, scope, simulation)

    def _collect(information, scope: str, simulation) -> None:
        """
        Run all the collectors for the given component.

        Args:
            information: Information object to collect data from.
            component: Component to collect data from.
            simulation: Simulation object to collect data from.
        """
        for name, func in information.collectors[scope].items():

            if callable(func):
                information.data[scope][name].append(func(simulation))
            else:

                if func[1] is None:
                    information.data[scope][name].append(
                        func[0](simulation))
                else:
                    information.data[scope][name].append(
                        func[0](simulation, **func[1]))
