import networkx as nx
from sdk.dooder import Dooder
from sdk.strategies.strategies import Strategies

""" 
Graph:
    nodes: dooders (id, age, position, object_ref)
    edges: interactions (cycle number, involved dooders, interaction type) & overall count per dooder
"""

seed_strategy = {
    'SeedCount': {
        'type': 'Generation',
        'function': 'uniform_distribution',
        'args': {
            'low': 10,
            'high': 15
        }
    },
    'SeedPlacement': {
        'type': 'Placement',
        'function': 'random_location',
        'args': {}
    },
    'SeedGenetics': {
        'type': 'Genetics',
        'function': 'random_genetics'
    }
}


dooder_strategy = {
    'StartingEnergySupply': {
        'function': 'uniform_distribution',
        'args': {
            'low': 10,
            'high': 15
        }
    },
    'MaxEnergySupply': {
        'function': 'normal_distribution',
        'args': {
            'mean': 50,
            'std': 10
        }
    },
    'Metabolism': {
        'function': 'uniform_distribution',
        'args': {
            'low': 1,
            'high': 5
        }
    },
    'SurvivalProbability': {
        'function': 'fixed_value',
        'args': {
            'value': 0.5
        }
    },
    'ReproductionProbability': {
        'function': 'fixed_value',
        'args': {
            'value': 0.5
        }
    },
    'ReproductionEnergyCost': {
        'function': 'fixed_value',
        'args': {
            'value': 10
        }
    },
    'ReproductionSuccessProbability': {
        'function': 'fixed_value',
        'args': {
            'value': 0.5
        }
    },
    'MoveProbability': {
        'function': 'fixed_value',
        'args': {
            'value': 0.5
        }
    },
    'MoveSuccessProbability': {
        'function': 'fixed_value',
        'args': {
            'value': 0.5
        }
    },
    'MoveEnergyCost': {
        'function': 'fixed_value',
        'args': {
            'value': 1
        }
    }
}


class Society:

    active_dooders = {}
    graph = nx.Graph()
    total_created_dooders = 0

    def __init__(self, simulation):
        self.simulation = simulation

    def generation_strategy(self, variable):
        #! maybe make this a more general function inside the Strategies class
        #! call it compile_strategy or something
        #! maybe compile all at once?????
        #! or make it a class method decorator?
        strat = seed_strategy[variable]['function']
        args = seed_strategy[variable]['args']
        func = Strategies.get(strat, 'Generation')

        return round(func(**args))

    def placement_strategy(self, number):
        strat = seed_strategy['SeedPlacement']['function']
        func = Strategies.get(strat, 'Placement')
        args = (self.simulation, number)

        return func(*args)

    def generate_seed_population(self):
        seed_count = self.generation_strategy('SeedCount')
        seed_placement = self.placement_strategy(seed_count)

        for position in seed_placement:
            self.generate_dooder(position, None)

    def generate_dooder(self, position, dooder_strategy):
        #! need to fix the dooder object creation and simplify it
        #! maybe make a dooder factory class or input dict
        dooder = Dooder(self.simulation.generate_id(), position,
                        self.simulation, dooder_strategy)
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
