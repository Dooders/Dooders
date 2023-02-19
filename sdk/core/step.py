""" 
Core: Step
----------
Core system for the Step Logic
"""

from abc import ABC, abstractmethod

from sdk.core import CoreComponent


class Step(CoreComponent):
    """ 
    A step is a point in the simulation to execute logic 
    for a specific object or model during its turn.

    Attributes
    ----------
    registry : dict
        A dictionary of all the registered step flows, 
        by the type of python object

    Methods
    -------
    register(type: str) -> Callable
        Register a step flow through a decorator
    forward(name: str, object: str) -> None
        Execute a step flow
    """

    @classmethod
    def forward(cls, name: str, object: str) -> None:
        """ 
        Execute a step flow

        Parameters
        ----------
        name : str
            The name of the step flow to execute
        object : object
            The object to execute the step flow on
        """
        steps = Core.get_component(
            'sdk.steps', object.__class__.__name__.lower())
        step_flow = steps[name].function
        step_flow.step(object)


class StepLogic(ABC):
    """ 
    Abstract Class for every step flow
    """

    def react(self, *args, **kwargs) -> None:
        """ 
        Optional method to react to the environment before acting

        Parameters
        ----------
        object : object
            The object that needs to react before acting
        """
        pass

    @abstractmethod
    def act(self, *args, **kwargs) -> None:
        """ 
        Required method to execute the action phase of the step flow

        Parameters
        ----------
        object : object
            The object that needs to act. Passed during the objects turn
        """
        raise NotImplementedError('act method not implemented')

    def sleep(self, *args, **kwargs) -> None:
        """ 
        Optional method to sleep after acting

        Parameters
        ----------
        object : object
            The object that needs to sleep after acting
        """
        pass

    @classmethod
    def step(cls, object: object) -> None:
        """ 
        Execute the step flow

        Parameters
        ----------
        object : object
            The object to execute the step flow on
        """
        cls.react(object)
        cls.act(object)
        cls.sleep(object)
