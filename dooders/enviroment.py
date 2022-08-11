from mesa.space import MultiGrid

from dooders.dooder import Energy  # bring this over


class Environment(MultiGrid):

    def __init__(self, width: int, height: int, torus: bool = True) -> None:
        """
        Create a new MultiGrid object.

        Args:
            width, height: The size of the grid to create.
            torus: Boolean whether the grid wraps or not.
        """
        super().__init__(width, height, torus)
        self.energy_landscape = {}
        self.energy_count = 0
        self.energy_ticker = 0

    def create_energy(self, starting_value: int, unique_id: int, location: tuple, simulation) -> Energy:
        """
        Create a new energy at the given location.

        Args:
            starting_value: The starting value of the energy.
            unique_id: The unique ID of the energy.
            pos: The position of the energy.
            simulation: The simulation object.

        Returns:
            The new energy object.
        """
        energy = Energy(starting_value, unique_id, location, simulation)
        self.energy_landscape.update(
            {'energy_' + str(self.energy_ticker): energy})
        self.energy_count += 1
        self.energy_ticker += 1

        return energy

    def consume_energy(self, energy: Energy) -> None:
        """
        Consume an energy.

        Args:
            energy: The energy to consume.
        """
        self.energy_landscape.pop(str(energy.unique_id))
        self.energy_count -= 1
