

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

class GenericChoice:
    effect = 'positive' # positive, negative, neutral
    target = 'self' # self, other, environment
    attributes = ['Strength']
    criteria = (threshold,('Strength', '>', 70))
    on_fail = (update_attribute,('Strength', -10))
    on_success = (update_attribute,('Strength', 10))


