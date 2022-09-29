"""

#TODO Finishing graph nodes and edges
#TODO Build in saving of dooder after each step (temporal storage)

Graph:
    nodes: dooders (id, age, position, object_ref)
    edges: interactions (cycle number, involved dooders, interaction type) 
        & overall count per dooder
        
"""

from typing import TYPE_CHECKING

import networkx as nx
from sdk.data import Position, UniqueID
from sdk.dooder import Dooder
from sdk.core.strategy import Strategies, compile_strategy

if TYPE_CHECKING:
    from sdk.base.base_simulation import BaseSimulation


SeedStrategy = Strategies.load_strategy('sdk/dooder/seed.yml')


class Society:
    """ 

    """

    active_dooders = {}
    graph = nx.Graph()
    total_created_dooders = 0
    graveyard = {}

    def __init__(self, simulation: 'BaseSimulation') -> None:
        """ 
        Args:
            simulation (BaseSimulation): simulation object

        Attributes:
            SeedPlacement (list): list of positions to place seed dooders
            SeedStrategy (dict): strategy to use for seed dooders

        """
        self.simulation = simulation
        self.seed = compile_strategy(self, SeedStrategy)

    def generate_seed_population(self) -> None:
        """
        Generate seed population
        """

        for position in self.SeedPlacement:
            self.generate_dooder(position)

    def generate_dooder(self, position: 'Position') -> None:
        """
        Generate a new dooder

        Args:
            position (tuple): position to place dooder
        """
        dooder = Dooder(self.simulation.generate_id(), position,
                        self.simulation)
        self.place_dooder(dooder, position)

    def place_dooder(self, dooder: 'Dooder', position: 'Position') -> None:
        """
        Place dooder in environment

        Args:
            dooder (Dooder): dooder object
            position (tuple): position to place dooder
        """
        self.simulation.environment.place_object(dooder, position)
        self.simulation.time.add(dooder)

        self.active_dooders[dooder.unique_id] = dooder

        # ! add dooder attributes to node
        self.graph.add_node(dooder.unique_id)
        self.total_created_dooders += 1

    def terminate_dooder(self, dooder: 'Dooder') -> None:
        """
        Terminate dooder based on the ID
        Removes from active_dooders, environment, and graph

        Args:
            dooder_id (str): dooder id
        """
        self.graveyard[dooder.unique_id] = dooder
        self.active_dooders.pop(dooder.unique_id)
        self.simulation.time.remove(dooder)
        self.simulation.environment.remove_object(dooder)

    def get_dooder(self, dooder_id: 'UniqueID') -> 'Dooder':
        """
        Get dooder based on the ID

        Args:
            dooder_id (str): dooder id

        Returns:
            Dooder: dooder object
        """
        return self.active_dooders[dooder_id]

    @property
    def active_dooder_count(self) -> int:
        """
        Get the number of active dooders

        Returns:
            int: number of active dooders
        """
        return len(self.active_dooders)

    @property
    def total_dooder_count(self) -> int:
        """
        Get the total number of dooders created

        Returns:
            int: total number of dooders created
        """
        return self.total_created_dooders
