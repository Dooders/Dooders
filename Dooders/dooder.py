from dooders.agent import RandomWalker
from dooders.behavior import Behavior


class Dooder(RandomWalker):
    """
    """

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.behavior = Behavior()

    def kill(self, agent):
        self.model.grid.remove_agent(agent)
        self.model.schedule.remove(agent)

    def die(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def step(self):
        # move --> action
        print(self.unique_id)
        self.random_move()


# def _spawn_attribute(attribute_range, weights):
#     return random.choices(attribute_range, weights, k=1)[0]

# def spawn_attributes(attribute_list, attribute_range, weights):
#     spawned_attributes = dict()
#     for attribute in attribute_list:
#         spawned_attributes[attribute] = _spawn_attribute(attribute_range, weights)

#     return spawned_attributes


# class Dooder:
#     def __init__(self):
#         self.birth_date = Reality.counter
#         self.name = names.get_full_name()
#         self.motivation = ''
#         self.base_attributes = spawn_attributes(ATTRIBUTE_LIST, Reality.attribute_range, Reality.weights)
#         self.attributes = self.base_attributes
