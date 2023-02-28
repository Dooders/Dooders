from dooders.sdk.actions import *
from dooders.sdk.core.core import _COMPONENTS
from dooders.sdk.core.step import *
from dooders.sdk.core.variables import Variables
from dooders.sdk.policies import *
from dooders.sdk.steps import *
from dooders.sdk.strategies import *


#! Do I still need this class????
class Configure:
    """ 
    Configure class for the SDK.
    
    Methods
    -------
    settings(type: str = None) -> dict
        Set a setting value.
    options() -> dict
        Discover all core components and settings.
    discover_components() -> dict
        Discover all core component functions.
    """
    
    @classmethod
    def settings(cls, type: str = None) -> dict:
        """ 
        Set a setting value 
        
        Parameters
        ----------
        type: str, optional
            The type of setting to set.
            
        Returns
        -------
        dict
            The settings that were requested.
            
        Examples
        --------
        >>> from sdk.core.configure import Configure
        >>>
        >>> Configure.settings()
        {'components': {'actions': {'action': ['Action', 'ActionStep', 'ActionStrategy', 'ActionPolicy']}, 'strategies': {'strategy': ['Strategy', 'StrategyStep', 'StrategyPolicy']}, 'steps': {'step': ['Step', 'StepStrategy', 'StepPolicy']}, 'policies': {'policy': ['Policy', 'PolicyStrategy']}}, 'variables': {'action': {'name': <sdk.core.settings.Variable object at 0x0000020B1B2B0D30>, 'description': <sdk.core.settings.Variable object at 0x0000020B1B2B0D68>, 'type': <sdk.core.settings.Variable object at 0x0000020B1B2B0DA0>, 'function': <sdk.core.settings.Variable object at 0x0000020B1B2B0DD8>, 'args': <sdk.core.settings.Variable object at 0x0000020B1B2B0E10>, 'kwargs': <sdk.core.settings.Variable object at 0x0000020B1B2B0E48>, 'step': <sdk.core.settings.Variable object at 0x0000020B1B2B0E80>, 'strategy': <sdk.core.settings.Variable object at 0x0000020B1B2B0EB8>, 'policy': <sdk.core.settings.Variable object at 0x0000020B1B2B0EF0>}, 'strategy': {'name': <sdk.core.settings.Variable object at 0x0000020B1B2B0F28>, 'description': <sdk.core.settings.Variable object at 0x0000020B1B2B0F60>, 'type': <sdk.core.settings.Variable object at 0x0000020B1B2B0F98>, 'function': <sdk.core.settings.Variable object at 0x0000020B1B2B0FD0>, 'args': <sdk.core.settings.Variable object at 0x0000020B1B2B8048>, 'kwargs': <sdk.core.settings.Variable object at 0x0000020B1B2B8080>, 'step': <sdk.core.settings.Variable object at 0x0000020B1B2B80B8>, 'policy': <sdk.core.settings.Variable object at 0x
        """
        if type is None:
            return cls.options()
        else:
            return cls.options()[type]
    
    @classmethod
    def options(self) -> dict:
        """ 
        Discover all core components and settings 
        
        Returns
        -------
        dict
            A dictionary of all core components and settings.
            
        Examples
        --------
        >>> from sdk.core.configure import Configure
        >>>
        >>> Configure.options()
        {'components': {'actions': {'action': ['Action', 'ActionStep', 'ActionStrategy', 'ActionPolicy']}, 'strategies': {'strategy': ['Strategy', 'StrategyStep', 'StrategyPolicy']}, 'steps': {'step': ['Step', 'StepStrategy', 'StepPolicy']}, 'policies': {'policy': ['Policy', 'PolicyStrategy']}}, 'variables': {'action': {'name': <sdk.core.settings.Variable object at 0x0000020B1B2B0D30>, 'description': <sdk.core.settings.Variable object at 0x0000020B1B2B0D68>, 'type': <sdk.core.settings.Variable object at 0x0000020B1B2B0DA0>, 'function': <sdk.core.settings.Variable object at 0x0000020B1B2B0DD8>, 'args': <sdk.core.settings.Variable object at 0x0000020B1B2B0E10>, 'kwargs': <sdk.core.settings.Variable object at 0x0000020B1B2B0E48>, 'step': <sdk.core.settings.Variable object at 0x0000020B1B2B0E80>, 'strategy': <sdk.core.settings.Variable object at 0x0000020B1B2B0EB8>, 'policy': <sdk.core.settings.Variable object at 0x0000020B1B2B0EF0>}, 'strategy': {'name': <sdk.core.settings.Variable object at 0x0000020B1B2B0F28>, 'description': <sdk.core.settings.Variable object at 0x0000020B1B2B0F60>, 'type': <sdk.core.settings.Variable object at 0x0000020B1B2B0F98>, 'function': <sdk.core.settings.Variable object at 0x0000020B1B2B0FD0>, 'args': <sdk.core.settings.Variable object at 0x0000020B1B2B8048>, 'kwargs': <sdk.core.settings.Variable object at 0x0000020B1B2B8080>, 'step': <sdk.core.settings.Variable object at 0x0000020B1B2B80B8>, 'policy': <sdk.core.settings.Variable object at 0x
        """
        return {
            'components': self.discover_components(),
            'variables': Variables.discover()
        }
    
    @classmethod
    def discover_components(self) -> dict:
        """ 
        Discover all core component functions 
        
        Returns
        -------
        dict
            A dictionary of all core component functions.
        
        Examples
        --------
        >>> from sdk.core.configure import Configure
        >>>
        >>> Configure.discover_components()
        {'actions': {'action': ['Action', 'ActionStep', 'ActionStrategy', 'ActionPolicy']}, 'strategies': {'strategy': ['Strategy', 'StrategyStep', 'StrategyPolicy']}, 'steps': {'step': ['Step', 'StepStrategy', 'StepPolicy']}, 'policies': {'policy': ['Policy', 'PolicyStrategy']}}
        """
        component_options = {}

        for component, modules in _COMPONENTS.items():
            component_dict = {}

            for module, functions in modules.items():
                component_dict[module] = {}
                options = []

                for function in functions:
                    options.append(function)

                component_dict[module] = options

            component_options[component] = component_dict

        return component_options
    