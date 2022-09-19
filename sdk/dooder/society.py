import networkx as nx
from sdk.dooder import Dooder
from sdk.strategies.strategies import BaseStrategy, compile_strategy, Strategies

""" 
Graph:
    nodes: dooders (id, age, position, object_ref)
    edges: interactions (cycle number, involved dooders, interaction type) & overall count per dooder
"""


SeedStrategy = Strategies.load_strategy('sdk/dooder/seed.yml')

class SeedStrategy:
    SeedCount = BaseStrategy(StrategyType='Generation', 
                             StrategyFunc='uniform_distribution',
                             Args={'low': 10, 'high': 15})
    
    SeedPlacement = BaseStrategy(StrategyType='Placement', 
                                 StrategyFunc='random_location',
                                 Args=None, 
                                 Dependency='SeedCount')


class Society:

    active_dooders = {}
    graph = nx.Graph()
    total_created_dooders = 0

    def __init__(self, simulation):
        self.simulation = simulation
        compile_strategy(self, SeedStrategy)

    def generate_seed_population(self):

        for position in self.SeedPlacement:
            self.generate_dooder(position, None)

    def generate_dooder(self, position, dooder_strategy):
        #! need to fix the dooder object creation and simplify it
        #! maybe make a dooder factory class or input dict
        dooder = Dooder(self.simulation.generate_id(), position,
                        self.simulation)
        self.place_dooder(dooder, position)

    def place_dooder(self, dooder, position):
        self.simulation.environment.place_object(dooder, position)
        self.simulation.time.add(dooder)

        self.active_dooders[dooder.unique_id] = dooder
        # ! add dooder attributes to node
        self.graph.add_node(dooder.unique_id)
        self.total_created_dooders += 1

    def terminate_dooder(self, dooder_id):
        self.active_dooders.pop(dooder_id)
        self.simulation.time.remove(dooder_id)
        self.simulation.environment.remove_object(dooder_id)

    def get_dooder(self, dooder_id):
        return self.active_dooders[dooder_id]

    @property
    def active_dooder_count(self):
        return len(self.active_dooders)

    @property
    def total_dooder_count(self):
        return self.total_created_dooders
