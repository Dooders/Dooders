""" 
"""
from random import choice
from typing import TYPE_CHECKING

import numpy as np

from dooders.sdk.base.base_policy import BasePolicy
from dooders.sdk.core.core import Core
    
    
@Core.register('policy')
class AutoEncoder(BasePolicy):
    
    @classmethod
    def execute(self, model_a, model_b) -> tuple:
        pass