
import random
import names
from reality import Reality

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
        self.birth_date = Reality.counter
        self.name = names.get_full_name()
        self.motivation = ''
        self.base_attributes = spawn_attributes(ATTRIBUTE_LIST, Reality.attribute_range, Reality.weights)
        self.attributes = self.base_attributes
