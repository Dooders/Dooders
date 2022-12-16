from typing import TYPE_CHECKING

import numpy as np

from sdk.base.base_policy import BasePolicy
from sdk.core.policies import Policies

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
        # {'move': {'consume': np.ndarray, 'reproduce': np.ndarray}}

        new_weights = {}
        weightsA = dooderA.internal_models.weights
        weightsB = dooderB.internal_models.weights

        for key in weightsA.keys():
            modelA = weightsA[key]
            modelB = weightsB[key]
            new_weights[key] = [(A + B) / 2 for A,B in zip(modelA, modelB)]

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
        new_weights = {}
        weightsA = dooderA.internal_models.weights
        weightsB = dooderB.internal_models.weights

        for key in weightsA.keys():
            modelA = weightsA[key]
            modelB = weightsB[key]

            new_weights[key] = {}

            for k in modelA.keys():
                mA = modelA[k]
                mB = modelB[k]
                new_weights[key][k] = [np.random.uniform(mA, mB)]

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
        new_weights = {}
        weightsA = dooderA.internal_models.weights
        weightsB = dooderB.internal_models.weights

        for key in weightsA.keys():
            modelA = weightsA[key]
            modelB = weightsB[key]

            new_weights[key] = {}

            for k in modelA.keys():
                mA = modelA[k]
                mB = modelB[k]
                new_weights[key][k] = [mA[0], mB[1]]

        return new_weights
