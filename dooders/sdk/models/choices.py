import inspect
import sys


def threshold(attribute, operator, value):
    """
    Returns a function that can be used as a filter for a query.
    """
    return lambda x: operator(getattr(x, attribute), value)


def update_attribute(attribute, value):
    """
    Subtract or add attribute by value
    """
    return lambda x: setattr(x, attribute, getattr(x, attribute) + value)


class Choice:
    possible_choices = dict()

    def __init__(self) -> None:
        self.get_choices()

    def compile_choices(self):
        return inspect.getmembers(sys.modules[__name__])

    def get_choice(self, name, choice_object):
        self.possible_choices[name] = choice_object

    def get_choices(self):
        for name, choice_object in self.compile_choices():
            if inspect.isclass(choice_object) and name != 'Choice':
                self.get_choice(name, choice_object)


class GenericChoice1:
    effect = 'positive'  # positive, negative, neutral
    target = 'self'  # self, other, environment
    attributes = ['Strength']
    criteria = (threshold, ('Strength', '>', 70))
    on_fail = (update_attribute, ('Strength', -10))
    on_success = (update_attribute, ('Strength', 10))


class GenericChoice2:
    effect = 'positive'  # positive, negative, neutral
    target = 'self'  # self, other, environment
    attributes = ['Intelligence']
    criteria = (threshold, ('Intelligence', '>', 70))
    on_fail = (update_attribute, ('Intelligence', -10))
    on_success = (update_attribute, ('Intelligence', 10))


class GenericChoice3:
    effect = 'negative'  # positive, negative, neutral
    target = 'self'  # self, other, environment
    attributes = ['Compassion', 'Luck']
    criteria = (threshold, ('Compassion', '>', 70))
    on_fail = (update_attribute, ('Compassion', -10))
    on_success = (update_attribute, ('Compassion', 10))
