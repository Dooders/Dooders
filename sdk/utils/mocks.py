from experiment import Experiment


def mock_simulation():
    config = {'Policies': {'Movement': 'NeuralNetwork'}, 'Simulation': {'MaxCycles':100}}
        
    experiment = Experiment(config)
    
    return experiment.simulation

def mock_dooder():
    sim = mock_simulation()
    sim.arena.generate_seed_population()
    dooder = sim.arena.active_dooders.values().__iter__().__next__()
    
    return dooder

def mock_energy():
    sim = mock_simulation()
    sim.resources.allocate_resources()
    energy = sim.resources.available_resources.values().__iter__().__next__()
    
    return energy
