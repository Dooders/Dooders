""" 
"""
from random import choice
from typing import TYPE_CHECKING

import numpy as np

from dooders.sdk.base.base_policy import BasePolicy
from dooders.sdk.core.core import Core
    
    
@Core.register('policy')
class AutoEncoder(BasePolicy):
    """ 
    Takes the weights of two models and encodes them
    into a single genetic layer weights
    """
    
    @classmethod
    def execute(self, model_a, model_b) -> tuple:
        """ 
        options: with anchoring, 
        either encoding twice or encoding 
        then averaging before decoding
        """
        pass