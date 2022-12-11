

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
        for type in self.keys():
            for name, model in self[type].items():
                model.inherit_weights(weights[type][name])
    
    @property
    def weights(self) -> dict:
        """ 
        Return a dictionary of weights from the internal models.
        
        Returns:
            dict: A dictionary of weights from the internal models.
        """
        model_types = self.keys()
        model_weights = dict()
        
        for type in model_types:
            model_weights[type] = dict()
            for name, model in self[type].items():
                model_weights[type][name] = model.weights
            
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
    
    