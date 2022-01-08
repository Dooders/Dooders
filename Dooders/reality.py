

def get_weights(weight_type='normal'):
    if weight_type == 'normal':
        upper_attribute_weights = list(reversed(range(1,51)))
        lower_attribute_weights = list(range(1,50))
        weights = lower_attribute_weights + upper_attribute_weights
        
    return weights

def get_attribute_range(start, stop):
    return list(range(start,stop))

class Reality:
    weights = get_weights()
    attribute_range = get_attribute_range(1,100)
    counter = 0