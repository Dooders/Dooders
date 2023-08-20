# Senses internal model for energy detection, dooder detection, hazard detection, etc.
# These output of these models are the input of the decision making model for movement

from pydantic import BaseModel


class Output:
    pass


class Senses(BaseModel):

    energy_detection = 'Energy'
    dooder_detection = 'Dooder'
    hazard_detection = 'Hazard'

    def execute(self):
        pass


# recursive and hierarchical thinking
def think(dooder, input):

    # loop through the attributes in the pattern
    result_list = list()

    for attribute in input.__fields__:
        model = dooder.internal_models(attribute)
        object_name = getattr(input(), attribute)
        perception_array = dooder.perception(object_name)

        result = model(perception_array)
        result_list.append(result)

        # model.learn(perception_array.True)

        if isinstance(result, Output):
            return result_list
        else:
            result_object =
            think(dooder, result)


class MoveDecision(Output):

    def __init__(self, dooder):
        outputs = think(dooder, Senses)
        model = dooder.internal_models('move_decision')


think(Senses)
