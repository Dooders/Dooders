

from collections import OrderedDict
from dooders.sdk.learning.scratch.model import SimpleNeuralNet

#! What is the best way to manage multiple internal models
#! And create them
#! Maybe just an ordered dict internal models with function to get weights
class Learning(OrderedDict):
    
    def __init__(self):
        super().__init__()