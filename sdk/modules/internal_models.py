from sdk.learning.nets.model import SimpleNeuralNet

class InternalModels(dict):
    """ 
    Work like a normal dictionary but with a method to easily replace
    the weights of the internal models.
    
    The InternalModels class models a Dooder's learned behaviors.
    """
    
    def __init__(self, model_list, *args, **kwargs) -> None:
        self.build(model_list)
        super(InternalModels, self).__init__(*args, **kwargs)
    
    def build(self, model_list):
        """
        
        """
        for model in model_list:
            self[model] = SimpleNeuralNet()
        
    def inherit_weights(self, weights: dict) -> None:
        """ 
        Take a dictionary of weights and inherit them into the internal models.
        
        Args:
            weights (dict): A dictionary of weights to inherit.
        """
        for model in self.keys():
            self[model].inherit_weights(weights[model])
    
    @property
    def weights(self) -> dict:
        """ 
        Return a dictionary of weights from the internal models.
        
        Returns:
            dict: A dictionary of weights from the internal models.
        """
        model_weights = dict()
        
        for model in self.keys():
            model_weights[model] = self[model].weights
            
        return model_weights
    
    @property
    def biases(self) -> dict:
        """ 
        Return a dictionary of biases from the internal models.
        
        Returns:
            dict: A dictionary of biases from the internal models.
        """
        keys = self.keys()
        biases = dict()
        
        for key in keys:
            biases[key] = self[key].biases
            
        return biases
    
    
