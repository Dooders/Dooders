# Energy

***This page is a work-in-progress***

Energy is a fundamental concept that measures the ability to perform work. 

In the context of this project, a Dooder's capacity to extract energy from the environment determines how much it can achieve and how long it can survive. Essentially, a Dooder requires energy to engage in movement and other actions.

This approach is in line with thermodynamics and how life on Earth is able to continue. In the simulation, Dooders must utilize energy to evade thermal equilibrium, which is akin to a terminal state or death. 

The second law of thermodynamics dictates that systems tend to gravitate toward equilibrium without an external source of energy, leading to their eventual demise. Similar to a hurricane gradually losing power until it dissipates entirely.

So, if a Dooder does not extract and consume energy from the environment, eventually it will be removed from the simulation.

## Types of Energy

### Simple Energy: 
Energy that is refreshed each cycle around the environment and can be consumed by all higher level energies.

### Local Energy: 
Energy that is locally bound in the environment that can be large but finite.

Also more difficult to extract this type of energy, but allows for large extractions over time

### Complex Energy: 
Energy with a limited ability to interact and learn that serves as an intermediary level where it consumes Simple Energy, but also can be consumed. This will give it predator-prey relationship with the Dooder agent.

Will be able to observe the evolution of this agent as well.
How it adapts to the Dooder dynamic.
I will also need to give this the ability to continue long into the simulation

## Highlights

* Used by dooders to move or perform actions
* Energy is added randomly at the start of each cycle
* Each Dooder has an energy supply
* After n cycles with no movement, 1 energy unit is taken from a dooder
* Energy dissipates at random intervals between min and max (laws)

## Future Ideas

* Energy creation cycles or periods. Like periods of plenty and scarcity
