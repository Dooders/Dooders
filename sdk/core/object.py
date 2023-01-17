# handle registering objects to use in the simulation
# this would allow to easily expand object types
# maybe include the base class to inherit, here as well


from abc import ABC


class Object(ABC):
    pass