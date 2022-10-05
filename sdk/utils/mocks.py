import yaml
from experiment import Experiment


def mock_simulation():
    with open('sdk/config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        
    experiment = Experiment(config)
    
    return experiment.simulation

def mock_dooder():
    sim = mock_simulation()
    sim.society.generate_seed_population()
    dooder = sim.society.active_dooders.values().__iter__().__next__()
    
    return dooder

def mock_energy():
    sim = mock_simulation()
    sim.resources.allocate_resources()
    energy = sim.resources.available_resources.values().__iter__().__next__()
    
    return energy
