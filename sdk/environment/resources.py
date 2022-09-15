from sdk.strategies.strategies import Strategies
from sdk.environment.energy import Energy

strategy = {
    'EnergyPerCycle': {'function': 'uniform_distribution', 'args': {'low': 1, 'high': 10}},
    'MaxTotalEnergy': {'function': 'normal_distribution', 'args': {'mean': 50, 'std': 10}},
    'EnergyLifespan': {'function': 'fixed_value', 'args': {'value': 7}},
    'EnergyPlacement': {'function': 'random_location'}
}

class Resources:
    
    available_resources = {}
    total_allocated_energy = 0
    
    def __init__(self, simulation):
        self.simulation = simulation

    def generation_strategy(self, variable):
        strat = strategy[variable]['function']
        args = strategy[variable]['args']
        func = Strategies.get(strat, 'Generation')
        
        return round(func(**args))


    def placement_strategy(self, simulation, number):
        strat = strategy['EnergyPlacement']['function']
        func = Strategies.get(strat, 'Placement')
        args = (simulation, number)

        return func(*args)
    
    def allocate_resources(self):
        energy_per_cycle = self.generation_strategy('EnergyPerCycle')
        max_total_energy = self.generation_strategy('MaxTotalEnergy')
        energy_lifespan = self.generation_strategy('EnergyLifespan')
        energy_placement = self.placement_strategy(self.simulation, energy_per_cycle)
        
        for location in energy_placement:
            if self.total_allocated_energy < max_total_energy:
                unique_id = self.simulation.generate_id()
                energy = Energy(unique_id, energy_lifespan, location)
                self.simulation.environment.place_object(energy, location)
                self.available_resources[unique_id] = energy
                self.total_allocated_energy += 1
                
    def step(self):
        for resource in self.available_resources.values():
            resource.step()
            
    def consume(self, resource):
        self.simulation.environment.remove_object(resource)
        self.available_resources.pop(resource.unique_id)
        
    def log(self, granularity, message, scope):
        self.simulation.log(granularity, message, scope)
        