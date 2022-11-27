from typing import TYPE_CHECKING

from sdk.base.base_policy import BasePolicy
from sdk.core.policies import Policies
import numpy as np

if TYPE_CHECKING:
    from sdk.models.dooder import Dooder
    

@Policies.register()
class AverageWeights(BasePolicy):
    """
    Taking the model weights from two Dooders and averaging them to use with a new Dooder.
    """

    @classmethod
    def execute(self, dooderA: 'Dooder', dooderB: 'Dooder') -> np.ndarray:
        """
        Averages the weights of two Dooders to create a new Dooder.

        Args:
            dooderA (Dooder): The first Dooder.
            dooderB (Dooder): The second Dooder.

        Returns:
            Dooder: The new Dooder weights
        """
        #! create model method to easily get layer weights
        new_weights = []
        for layerA, layerB in zip(dooderA.movement.weights, dooderB.movement.weights):
            new_weights.append((layerA + layerB) / 2)
        return new_weights


@Policies.register()
class RangeWeights(BasePolicy):
    """
    Taking the model weights from two Dooders and randomly selecting weights 
    between the range of the two Dooder to use with a new Dooder.
    """

    @classmethod
    def execute(self, dooderA: 'Dooder', dooderB: 'Dooder') -> np.ndarray:
        """
        Randomly selects weights between the range of the two Dooders to create a new Dooder.

        Args:
            dooderA (Dooder): The first Dooder.
            dooderB (Dooder): The second Dooder.

        Returns:
            Dooder: The new Dooder weights
        """
        #! create model method to easily get layer weights
        new_weights = []
        for layerA, layerB in zip(dooderA.movement.weights, dooderB.movement.weights):
            new_weights.append(np.random.uniform(layerA, layerB))
        return new_weights
        
        
@Policies.register()
class SplitWeights(BasePolicy):
    """
    Taking the model weights from two Dooders. The first layer weights of DooderA
    and the second layer weights from DooderB.
    Then use those weights in a new Dooder.
    """

    @classmethod
    def execute(self, dooderA: 'Dooder', dooderB: 'Dooder') -> np.ndarray:
        """
        Takes the first layer weights from DooderA and the second layer weights from DooderB.
        Then use those weights in a new Dooder.

        Args:
            dooderA (Dooder): The first Dooder.
            dooderB (Dooder): The second Dooder.

        Returns:
            Dooder: The new Dooder weights
        """
        #! create model method to easily get layer weights
        new_weights = []
        new_weights.append(dooderA.movement.weights[0])
        new_weights.append(dooderB.movement.weights[1])
        
        return new_weights
