# States

## Simulation state
* simulation_id: id given at the beginning of the simulation
* running: True/False if the simulation is running
* starting_time: Timestamp for when the simulation started
* ending_time: Timestamp for when the simulation ended
* arena: The arena state data
* environment: The environment state data
* information: All the data collected during the simulation

## Arena state
* active_dooders: a dictionary with all the Dooder agents still in the simulation (References the objects themselves)
* graveyard: A list of Dooder IDs for all agents terminated during the simulation (Contains only the string id, the object is deleted when terminated)

## Environment state
