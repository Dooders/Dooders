
import random
import names
import reality

from config import ATTRIBUTE_LIST



def _spawn_attribute(attribute_range, weights):
    return random.choices(attribute_range, weights, k=1)[0]

def spawn_attributes(attribute_list, attribute_range, weights):
    spawned_attributes = dict()
    for attribute in attribute_list:
        spawned_attributes[attribute] = _spawn_attribute(attribute_range, weights)
        
    return spawned_attributes


class Dooder:
    def __init__(self):
        self.birth_date = reality.counter
        self.name = names.get_full_name()
        self.motivation = ''
        self.base_attributes = spawn_attributes(ATTRIBUTE_LIST, reality.attribute_range, reality.weights)
        self.attributes = self.base_attributes
