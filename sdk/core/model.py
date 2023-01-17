# manager for models
# compile configs
# build models
# nice, clean, and modular

from abc import ABC, abstractmethod


# a model can:
# - step (required)
# - collect
# - setup
# - cleanup



#! this is more of a base class, 
#! a model manager class might be a good idea too
#! each model will inherit this
#! model manager will register models
class CoreModel(ABC):
    
    @abstractmethod
    def step(self):
        """ 
        Might be the only required method.
        Encompasses the logic for a single step of the model
        during a cycle in the simulation
        """
        raise NotImplementedError
    
    @abstractmethod
    def collect(self):
        """ 
        Might not need this method, but it's here
        in case we need to collect data from the
        model at each step
        """
        raise NotImplementedError
    
    @abstractmethod
    def setup(self):
        """ 
        Method for any actions that need to occur 
        at the beginning of the simulation
        """
        raise NotImplementedError
    
    @abstractmethod
    def cleanup(self):
        """ 
        Method for any actions that need to occur at 
        the end of the simulation
        """
        raise NotImplementedError