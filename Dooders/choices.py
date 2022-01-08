

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
    def __init__(self) -> None:
        self.possible_choices = dict()

    @classmethod
    def get_choices(cls):
        return [choice for choice in cls]

    def compile_choices():
        return inspect.getmembers(sys.modules[__name__])

    def add_choice(name, choice_object):
        available_choices[name] = choice_object
        
    def add_choices():
        for name, choice_object in compile_choices():
            if inspect.isclass(choice_object) and name != 'Choice':
                add_choice(name, choice_object)
class GenericChoice:
    effect = 'positive' # positive, negative, neutral
    target = 'self' # self, other, environment
    attributes = ['Strength']
    criteria = (threshold,('Strength', '>', 70))
    on_fail = (update_attribute,('Strength', -10))
    on_success = (update_attribute,('Strength', 10))

class GenericChoice2:
    effect = 'positive' # positive, negative, neutral
    target = 'self' # self, other, environment
    attributes = ['Intelligence']
    criteria = (threshold,('Intelligence', '>', 70))
    on_fail = (update_attribute,('Intelligence', -10))
    on_success = (update_attribute,('Intelligence', 10))
