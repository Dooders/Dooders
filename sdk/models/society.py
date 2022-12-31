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
from pydantic import BaseModel

from sdk.core import Strategy, compile_strategy
from sdk.models import Dooder

if TYPE_CHECKING:
    from sdk.base.base_simulation import BaseSimulation


SeedStrategy = Strategy.load_strategy('seed')


class Attributes(BaseModel):
    dooders_created: int = 0
    dooders_died: int = 0


class Society:
    """ 

    """

    def __init__(self, simulation: 'BaseSimulation') -> None:
        """ 
        Args:
            simulation (BaseSimulation): simulation object

        Attributes:
            SeedPlacement (list): list of positions to place seed dooders
            SeedStrategy (dict): strategy to use for seed dooders

        """
        self.graph = nx.Graph()
        self.active_dooders = {}
        self.graveyard = {}
        self.history = {}
        self.simulation = simulation
        self.seed = compile_strategy(self, SeedStrategy)
        self.reset()

    def step(self) -> None:
        """
        Step the society forward
        """
        self.reset()

    def reset(self) -> None:
        """
        reset main attributes
        """
        for attribute in Attributes():
            setattr(self, attribute[0], attribute[1])

    def generate_seed_population(self) -> None:
        """
        Generate seed population
        """
        for position in self.SeedPlacement:
            self.generate_dooder(position)

    def _generate_dooder(self, position) -> 'Dooder':
        """
        Generate a new dooder

        Args:
            position (tuple): position to place dooder

        Returns:
            Dooder: dooder object
        """
        dooder = Dooder(self.simulation.generate_id(),
                        position, self.simulation)
        return dooder

    def generate_dooder(self, position) -> None:
        """
        Generate a new dooder and place it

        Args:
            position (tuple): position to place dooder
        """
        dooder = self._generate_dooder(position)
        self.place_dooder(dooder, position)
        # ! remove duplicate log call
        dooder.log(granularity=1,
                   message=f"Created {dooder.unique_id}", scope='Dooder')

    def place_dooder(self, dooder: 'Dooder', position) -> None:
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
        #! WIP
        self.graph.add_node(dooder.unique_id)
        self.dooders_created += 1

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
        self.dooders_died += 1

    def get_dooder(self, dooder_id=None) -> 'Dooder':
        """
        Get dooder based on the ID

        Args:
            dooder_id (str): dooder id

        Returns:
            Dooder: dooder object
        """

        if dooder_id is None:
            if len(self.active_dooders) == 0:
                return self.simulation.random.choice(list(self.graveyard.values()))
            else:
                return self.simulation.random.choice(list(self.active_dooders.values()))
        else:

            return self.active_dooders[dooder_id]

    @property
    def active_dooder_count(self) -> int:
        """
        Get the number of active dooders

        Returns:
            int: number of active dooders
        """
        return len(self.active_dooders)
