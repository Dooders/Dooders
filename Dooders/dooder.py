import math

from mesa import Agent

from dooders.base import BaseDooder
from dooders.behavior import ask_fate

# class BaseMessage(BaseModel):
#     unique_id: int
#     experiment_id: str
#     cycle: int
#     verbosity: int
#     prefix = f"{experiment_id} - {cycle} - {verbosity} - "




# class DieMessage(BaseMessage):
#     "Have it inherit and do it right"
#     reason: str
#     base_message = f"Dooder {unique_id} died from {reason}"

    


def get_direction(origin: tuple, destination: tuple) -> str:
    """
    Get the direction from one position to another.
    
    Args:
        origin: The (x, y) position of the origin
        destination: The (x, y) position of the destination
        
    Returns:
        The direction from the origin to the destination
     """
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    deltaX = destination[0] - origin[0]
    deltaY = destination[1] - origin[1]

    degrees = math.atan2(deltaX, deltaY)/math.pi*180
    if degrees < 0:
        degrees_final = 360 + degrees
    else:
        degrees_final = degrees

    compass_lookup = round(degrees_final / 45)

    return compass_brackets[compass_lookup]


class Dooder(BaseDooder):

    def __init__(self, unique_id: int, position: tuple, model, moore=True):
        """
        Create a new Dooder agent.

        Args:
            unique_id: Unique ID for the agent.
            position: Starting position for the agent.
            model: Reference to the model.
        """
        super().__init__(unique_id, position, model)
        self.energy = 5
        self.direction = 'Origin'
        self.position = position
        self.moore = moore
        self.log(granularity=1, message=f"Agent {self.unique_id} created")
    
    def kill(self, dooder: BaseDooder):
        """ 
        Kill a dooder. 
        
        Args:
            dooder: The dooder to kill.
        """
        self.model.environment.remove_agent(dooder)
        self.model.schedule.remove(dooder)
        message = f"Agent {self.unique_id} killed {dooder.unique_id}"

        self.log(granularity=1, message=message)

    def die(self, reason='Unknown'):
        """
        A dooder dies.

        Args:
            reason: The reason for the death.
        """
        self.model.environment.remove_agent(self)
        self.model.schedule.remove(self)
        message = f"Agent {self.unique_id} died from {reason}"

        self.log(granularity=1, message=message)

    def choose_random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        possible_moves = self.model.environment.get_neighborhood(
            self.position, self.moore, True)

        origin = self.position
        destination = self.random.choice(possible_moves)

        return origin, destination

    def step(self):
        """
        """
        # get cell contents
        direction= 'None'
        cell_contents = self.model.environment.get_cell_list_contents(self.position)
        energy = [obj for obj in cell_contents if isinstance(obj, Energy)]

        if len(energy) > 0:
            self.energy += 1
            energy[0].consume()

        if self.energy < 1:
            self.die('lack of energy')
            return

        if ask_fate(self.behavior.MakeMoveProbability):  # if true, move
            origin, destination = self.choose_random_move()

            if origin != None:
                new_direction = get_direction(origin, destination)
            else:
                new_direction = get_direction(self.position, destination)

            if ask_fate(self.behavior.MoveSuccessProbability):  # if true, successfuly move
                self.model.environment.move_agent(self, destination)
                self.energy -= 1
                direction = new_direction
                self.position = destination
                self.log(granularity=2, message=f"Agent {self.unique_id} moved {direction} from {origin} to {destination}")
            else:
                self.energy -= 1
                self.log(granularity=3, message=f"Agent {self.unique_id} failed to move {direction} from {origin} to {destination}")
        else:
            direction = 'None'
            self.log(granularity=3, message=f"Agent {self.unique_id} skipped move")

        self.direction = direction

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


class Energy(Agent):
    def __init__(self, unique_id, position, model):
        """
        Create a new Energy agent.

        Args:
            unique_id: Unique ID for the agent.
            position: Starting position for the agent.
            model: Reference to the model.
        """
        super().__init__(unique_id, model)
        self.position = position

    def consume(self):
        self.model.environment.consume_energy(self)

    