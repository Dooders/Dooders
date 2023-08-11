""" 
Dooder Step Flows
-----------------
Collection of step flows for dooders
"""

from dooders.sdk.core.core import Core
from dooders.sdk.core.step import StepLogic


@Core.register('step')
class BasicStep(StepLogic):
    """ 
    Step flow for a dooder.

    The Dooder will first move, then consume, then reproduce.
    """

    __description__ = ''

    def act(dooder):
        dooder.do('move')
        dooder.do('consume')
        # dooder.do('reproduce')
