from typing import Callable


class BaseCore:
    """ 
    The factory class to be used as a decorator to register a stop condition. 
    """
    
    def infer_scope(self, component: Callable) -> str:
        """ 
        Infer the purpose based on the filename

        """
        return component.__module__.split('.')[-1]

    def get_scope(self, scope):
        for purpose in self.registry:
            if scope in self.registry[purpose]:
                return purpose
        return None
