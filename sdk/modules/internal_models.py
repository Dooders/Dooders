

class InternalModels(dict):
    """ 
    Work like a normal dictionary but with a method to easily replace
    the weights of the internal models.
    """
    
    def __init__(self, *args, **kwargs):
        super(InternalModels, self).__init__(*args, **kwargs)
        
    def inherit_weights(self, weights):
        """ 
        Take a dictionary of weights and inherit them into the internal models.
        """
        pass
    
    @property
    def weights(self):
        """ 
        Return a dictionary of weights from the internal models.
        
        """
        pass
    
    @property
    def biases(self):
        """ 
        Return a dictionary of biases from the internal models.
        """
        pass
    
    