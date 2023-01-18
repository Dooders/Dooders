""" 
Dooder Step Flows
-----------------
Collection of step flows for dooders
"""

from sdk.core.step import Step, StepLogic

@Step.register('Dooder')
class BasicStep(StepLogic):
    """ 
    Step flow for a dooder.
    
    The Dooder will first move, then consume, then reproduce.
    """

    __description__ = ''
    
    def act(dooder):
        dooder.do('move')
        dooder.do('consume')
        dooder.do('reproduce')
