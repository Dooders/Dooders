

class InternalModels(dict):
    """ 
    Work like a normal dictionary but with a method to easily replace
    the weights of the internal models.
    
    The InternalModels class models a Dooder's learned behaviors.
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super(InternalModels, self).__init__(*args, **kwargs)
        
    def inherit_weights(self, weights: dict) -> None:
        """ 
        Take a dictionary of weights and inherit them into the internal models.
        
        Args:
            weights (dict): A dictionary of weights to inherit.
        """
        for key in self.keys():
            self[key].inherit_weights(weights[key])
    
    @property
    def weights(self) -> dict:
        """ 
        Return a dictionary of weights from the internal models.
        
        Returns:
            dict: A dictionary of weights from the internal models.
        """
        keys = self.keys()
        weights = dict()
        
        for key in keys:
            weights[key] = self[key].weights
            
        return weights
    
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
    
    