from sdk.base_object import BaseObject
from sdk.dooder.behavior import Behavior, ask_fate
from sdk.dooder.cognition import Cognition
from sdk.dooder.util import get_direction
from sdk.environment.energy import Energy


class Dooder(BaseObject):
    """ 

    """

    def __init__(self, unique_id: int, position: tuple, simulation, params: dict) -> None:
        """
        Create a new Dooder object.

        Args:
            unique_id: Unique ID for the object.
            position: Starting position for the object.
            simulation: Reference to the simulation.
            params: Parameters for the simulation.

        Attributes:
            unique_id: Unique ID for the object.
            position: Starting position for the object.
            simulation: Reference to the simulation.
            params: Parameters for the simulation.
            energy: The energy level of the dooder.
            direction: The direction the dooder is facing.
            moore: The Moore neighborhood of the dooder.
            cognition: The cognition of the dooder.
            behavior: The behavior of the dooder.
        """
        super().__init__(unique_id, position, simulation)
        self.behavior = Behavior()
        self.cognition = Cognition()
        self.params = params
        self.energy = self.params.StartingEnergySupply
        self.direction = 'Origin'
        self.moore = self.params.Moore
        self.log(granularity=1,
                 message=f"Created", scope='Dooder')

    def kill(self, dooder: BaseObject) -> None:
        """ 
        Kill a dooder. 

        Args:
            dooder: The dooder to kill.
        """
        self.simulation.environment.remove_object(dooder)
        self.simulation.time.remove(dooder)
        message = f"Killed {dooder.unique_id}"

        self.log(granularity=1, message=message, scope='Dooder')

    def die(self, reason: str = 'Unknown') -> None:
        """
        A dooder dies.

        Args:
            reason: The reason for the death.
        """
        self.simulation.environment.remove_object(self)
        self.simulation.time.remove(self)
        message = f"Died from {reason}"

        self.log(granularity=1, message=message, scope='Dooder')

    def choose_random_move(self) -> tuple:
        """
        Step one cell in any allowable direction.

        Returns:
            origin: The origin of the move.
            destination: The destination after the move.
        """
        # Pick the next cell from the adjacent cells.
        possible_moves = self.simulation.environment.get_neighborhood(
            self.position, self.moore, True)

        origin = self.position
        destination = self.random.choice(possible_moves)

        return origin, destination

    def step(self) -> None:
        """
        Step the dooder.
        """
        #! Come up with a better design step flow.
        # get cell contents
        direction = 'None'
        cell_contents = self.simulation.environment.get_cell_list_contents(
            self.position)
        energy = [obj for obj in cell_contents if isinstance(obj, Energy)]

        if isinstance(energy, Energy):
            self.energy += 1
            energy[0].consume()

        elif len(energy) == 1:
            self.energy += 1
            e = energy[0]
            e.consume()
            self.log(
                granularity=2, message=f"Consumed energy: {e.unique_id}", scope='Dooder')

        elif len(energy) == 0:
            pass

        else:
            pass

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
                self.simulation.environment.move_object(self, destination)
                self.energy -= 1
                direction = new_direction
                self.position = destination
                self.log(
                    granularity=2, message=f"Moved {direction} from {origin} to {destination}", scope='Dooder')
            else:
                self.energy -= 1
                self.log(
                    granularity=3, message=f"Failed to move {direction} from {origin} to {destination}", scope='Dooder')
        else:
            direction = 'None'
            self.log(
                granularity=3, message=f"Skipped move", scope='Dooder')

        self.direction = direction
