from typing import TYPE_CHECKING

from sdk.base.base_policy import BasePolicy
from sdk.core.policies import Policies

if TYPE_CHECKING:
    from sdk.models.dooder import Dooder
    
    
#! Need different methods to reproduce (Average of weights, random number between parent weights, etc.)

@Policies.register()
class NeuralNetwork(BasePolicy):
    """

    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        pass
        