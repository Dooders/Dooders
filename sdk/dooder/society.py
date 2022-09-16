import networkx as nx

from sdk.dooder import Dooder

""" 
SeedStrategy
    SeedCount
    SeedPlacement
    SeedGenetics
DooderStrategy
    StartingEnergySupply
    MaxEnergySupply
    Metabolism
    SurvivalProbability
    ReproductionProbability
    ReproductionEnergyCost
    ReproductionSuccessProbability
    MoveProbability
    MoveSuccessProbability
    MoveEnergyCost
    
    
Per dooder:
- position
- id

Graph:
    nodes: dooders (id, age, position, object_ref)
    edges: interactions (cycle number, involved dooders, interaction type) & overall count per dooder

"""


class Society:
    
    active_dooders = {}
    dooder_graph = nx.Graph()
    total_created_dooders = 0
    
    def __init__(self, simulation):
        self.simulation = simulation
    
    def generate_seed_population(self, seed_strategy):
        pass
    
    def generate_dooder(self, dooder_strategy):
        pass 
    
    def place_dooder(self, dooder_id, position):
        pass
    
    def terminate_dooder(self, dooder_id):
        pass
    
    def get_dooder(self, dooder_id):
        pass
    
    @property
    def active_dooder_count(self):
        return len(self.active_dooders)
    
    @property
    def total_dooder_count(self):
        return self.total_created_dooders