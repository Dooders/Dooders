""" 
Core: Step
----------
Core system for the Step Logic
"""

from abc import ABC, abstractmethod

from dooders.sdk.core.core import Core


class Step(Core):
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
    forward(name: str, object: str) -> None
        Execute a step flow
    """

    @classmethod
    def forward(cls, name: str, object: object) -> None:
        """ 
        Execute a step flow

        Parameters
        ----------
        name : str, (move, consume, etc.)
            The name of the step flow to execute
        object : object
            The object to execute the step flow on
            
        Examples
        --------
        >>> from sdk.core.step import Step
        >>>
        >>> Step.forward('move', agent)
        """
        steps = Core.get_component(
            'step', object.__class__.__name__.lower())
        step_flow = steps[name].function
        step_flow.step(object)


class StepLogic(ABC):
    """ 
    Abstract Class for every step flow
    
    Methods
    -------
    react(object: object) -> None
        Optional method to react to the environment before acting
    act(object: object) -> None
        Required method to execute the action phase of the step flow
    sleep(object: object) -> None
        Optional method to sleep after acting
    step(object: object) -> None
        Execute the step flow
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
            
        Raises
        ------
        NotImplementedError
            If the act method is not implemented
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
            
        Examples
        --------
        >>> from sdk.core.step import StepLogic
        >>>
        >>> class Move(StepLogic):
        >>>     def act(self, object):
        >>>         print('Moving')
        >>>
        >>> Move.step(agent)
        Moving
        """
        cls.react(object)
        cls.act(object)
        cls.sleep(object)
