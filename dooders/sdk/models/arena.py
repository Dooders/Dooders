"""
Arena Model
-------------
This module is responsible for the creation and management of Dooder objects 
within the environment.

The Dooder objects represent agents within the system and interact with the 
surrounding environment, known as the arena. The concept of the agent-arena 
relationship is derived from the work of John Vervaeke, a prominent scholar 
who emphasizes the dynamic interplay between agents and their environments.

According to Vervaeke's theory, the agent and the environment continually 
influence and shape each other through a cyclical feedback loop. As Dooder 
objects interact with the arena, they affect its state, while the arena, 
in turn, influences the behavior and characteristics of the Dooder objects. 
This mutual shaping process highlights the intricate relationship between 
agents and their surrounding environment.

By managing the creation and behavior of Dooder objects, this module 
facilitates the exploration and analysis of the agent-arena dynamics, 
enabling further investigation into the complex interdependencies between 
agents and their environments.
"""

from typing import TYPE_CHECKING, Generator

import networkx as nx
from pydantic import BaseModel
from sklearn.decomposition import PCA

from dooders.sdk.models import Dooder

if TYPE_CHECKING:
    from dooders.sdk.base.reality import BaseSimulation


gene_embedding = PCA(n_components=3)


class Attributes(BaseModel):
    dooders_created: int = 0
    dooders_died: int = 0


class Arena:
    """
    Class manages Dooder objects in the simulation.

    The class also keeps track of the total number of Dooders created and 
    terminated for each cycle. (The Information class will have historical 
    data for the above stats. The counts are reset after each cycle.) 

    Parameters
    ----------
    simulation : Simulation object
        The simulation object that contains the environment, agents, 
        and other models.

    Attributes
    ----------
    dooders_created : int
        The total number of Dooders created (for the current cycle).
    dooders_terminated: int
        The total number of Dooders terminated (for the current cycle).
    graph : networkx.Graph
        The graph object that contains the Dooder objects and relationships.
    active_dooders : dict
        Current active Dooders indexed by their unique id.
    graveyard : list
        Terminated Dooders IDs
    simulation: see ``Parameters`` section.
    seed : function
        The function that generates the seed population to start 
        the simulation.

    Methods
    -------
    _setup() -> None
        Setup the Arena. This will reset attributes.
    step() -> None
        Step the Arena forward. Currently, this will only reset attributes.
    reset() -> None
        Reset main attributes after each cycle.
    generate_seed_population() -> None
        Generate seed population based on the selected strategy.
    generate_dooder(position: tuple, tag: str = 'Seed') -> Dooder
        Generate a new dooder and place it in the environment
    place_dooder(dooder: Dooder, position: tuple) -> None
        Place a dooder in the environment
    _generate_dooder(position: tuple, tag: str = 'Seed') -> Dooder
        Generate a new dooder with a provided position
    terminate_dooder(dooder: Dooder) -> None
        Terminate a dooder
    get_dooder(dooder_id: str) -> Dooder
        Get a dooder by its unique id
    dooders() -> Generator[Dooder, None, None]
        Get all dooders in the environment
    collect_dooders() -> None
        Collect all stats from dooders

    Properties
    ----------
    active_dooder_count : int
        The number of active Dooders.
    state : dict
        The state of the Arena.
    weights : list
        The weights of all active Dooders.
    """

    total_counter = 0

    def __init__(self, simulation: 'BaseSimulation', settings) -> None:
        self.graph = nx.Graph()
        self.active_dooders = {}
        self.graveyard = {}
        self.simulation = simulation
        self.settings = settings

    def _setup(self) -> None:
        self.reset()  # set attributes

    def step(self) -> None:
        """
        Step the Arena forward. Currently, this will only reset attributes.
        """
        self.reset()

    def reset(self) -> None:
        """
        Reset main attributes after each cycle.
        """
        for attribute in Attributes():
            setattr(self, attribute[0], attribute[1])

    def generate_seed_population(self) -> None:
        """
        Generate seed population based on the selected strategy.
        """
        self.initial_dooder_count = self.settings.get('SeedCount')

        for position in self.SeedPlacement(self.initial_dooder_count):
            self.generate_dooder(position)

    def _generate_dooder(self, position: tuple, tag: str = 'Seed') -> 'Dooder':
        """
        Generate a new dooder with a provided position

        Parameters
        ----------
        position : tuple 
            position to place dooder, (x, y)

        Returns
        -------
        Dooder: dooder object
            Newly generated Dooder object
        """
        dooder = Dooder(self.simulation.generate_id(),
                        position, self.simulation)
        dooder.tag = tag
        dooder.gene_embedding = gene_embedding

        return dooder

    def generate_dooder(self, position: tuple) -> None:
        """
        Generate a new dooder and place it in the environment

        Parameters
        ----------
        position : tuple
            position to place dooder, (x, y)
        """
        dooder = self._generate_dooder(position)
        self.place_dooder(dooder, position)
        dooder.log(granularity=1,
                   message=f"Created {dooder.id}", scope='Dooder')

    def place_dooder(self, dooder: 'Dooder', position: tuple) -> None:
        """
        Place dooder in environment

        The method will also add the dooder to the active_dooders dictionary
        and add the dooder to the graph for relationship tracking.

        Parameters
        ----------
        dooder : Dooder object 
        position : tuple
            position to place dooder, (x, y)
        """
        self.simulation.environment.place_object(dooder, position)
        self.simulation.time.add(dooder)

        self.active_dooders[dooder.id] = dooder

        #! TODO: Add more attributes to graph node
        self.graph.add_node(dooder.id)
        self.dooders_created += 1
        self.total_counter += 1
        dooder.number = self.total_counter

    def terminate_dooder(self, dooder: 'Dooder') -> None:
        """
        Terminate dooder based on the unique id
        Removes from active_dooders, environment, and time

        Parameters
        ----------
        dooder_id : str
            dooder unique id, generated by the simulation
        """
        self.simulation.time.remove(dooder)
        self.simulation.environment.remove_object(dooder)
        self.active_dooders.pop(dooder.id)
        self.graveyard[dooder.id] = dooder.state
        self.dooders_died += 1
        del dooder

    def get_dooder(self, dooder_id: str = None) -> 'Dooder':
        """
        Get dooder based on the unique id, if no id is provided, a random dooder
        will be selected from the active dooders. If no active dooders are
        available, a random dooder will be selected from the graveyard.

        Parameters:
        ----------
        dooder_id : str
            dooder unique id, generated by the simulation

        Returns
        -------
        Dooder: dooder object
        """

        if dooder_id is None:
            if len(self.active_dooders) == 0:
                return self.simulation.random.choice(list(self.graveyard.values()))
            else:
                return self.simulation.random.choice(list(self.active_dooders.values()))
        else:
            return self.active_dooders[dooder_id]

    def dooders(self) -> Generator['Dooder', None, None]:
        """ 
        Generator that yields all active dooders

        Yields
        ------
        Dooder: dooder object
        """
        for dooder in self.active_dooders.values():
            yield dooder

    def collect(self) -> dict:
        """
        Collects the attributes of dooders for simulation statistics.

        Returns
        -------
        dict
            A dictionary of the dooders' attributes.
        """
        dooder_attributes = [
            (dooder.age, dooder.hunger, dooder.energy_consumed) for dooder in self.dooders()]
        dooder_count = len(dooder_attributes)

        def median(data: list) -> float:
            data = sorted(data)
            n = len(data)
            mid = n // 2
            return (data[mid] if n % 2 else (data[mid - 1] + data[mid]) / 2)

        if dooder_count > 0:
            ages, hunger, energy_consumed = zip(*dooder_attributes)
        else:
            ages, hunger, energy_consumed = [], [], []

        return {
            'active_dooder_count': self.active_dooder_count,
            'terminated_dooder_count': self.dooders_died,
            'created_dooder_count': self.dooders_created,
            'average_dooder_hunger': round(sum(hunger) / dooder_count, 3) if hunger else 0,
            'median_dooder_age': median(ages) if ages else 0,
            'average_dooder_age': round(sum(ages) / dooder_count, 3) if ages else 0,
            'average_energy_consumed': round(sum(energy_consumed) / dooder_count, 3) if energy_consumed else 0
        }

    @property
    def active_dooder_count(self) -> int:
        """ 
        Returns the number of active dooders
        """
        return len(self.active_dooders)

    @property
    def state(self) -> dict:
        """
        Returns the state of the Arena of all active dooders
        """
        return {**self.graveyard, **{k: v.state for k, v in self.active_dooders.items()}}

    @property
    def weights(self) -> dict:
        """
        Returns the weights of the Arena for all active dooders
        """
        return [v.weights for v in self.active_dooders.values()]

    @property
    def current_cycle(self) -> int:
        """
        Returns the current cycle of the simulation
        """
        return self.simulation.cycle_number
