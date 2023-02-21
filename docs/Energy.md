# Energy

***This page is a work-in-progress***

Energy is a fundamental object that allows an agent to stay in the simulation. 

In the context of this project, a Dooder's capacity to extract energy from the environment determines how long it can survive. Essentially, a Dooder requires energy to engage in movement and other actions.

This approach is in line with thermodynamics and how life on Earth started and evolved. The second law of thermodynamics dictates that systems tend to gravitate toward equilibrium (also called entropy[^1]) without an external source of energy, leading to their eventual demise. Similar to a hurricane gradually losing power until it dissipates entirely.

In the simulation, Dooders must utilize energy to evade thermal equilibrium, which is akin to a terminal state or death. 

## Types of Energy

### Simple Energy: 
Energy that is refreshed each cycle around the environment and can be consumed by all higher level energies.

* Consumed by Dooders and Complex Energy agents
* Allocation is managed by the [Resources](https://github.com/csmangum/Dooders/blob/main/sdk/models/resources.py) class.
* Worth 1 energy unit when consumed.
* Allocation is determined by its [placement strategy](https://github.com/csmangum/Dooders/blob/main/sdk/strategies/placement.py) each cycle.
* Has a limited lifespan based on Energy [settings](https://github.com/csmangum/Dooders/blob/main/sdk/variables/energy.yml), then it will remove itself from the environment.

### Local Energy: 
Energy that is locally bound in the environment that can be large but finite.

Also more difficult to extract this type of energy, but allows for large extractions over time

> Still in development

### Complex Energy: 
Energy with a limited ability to interact and learn that serves as an intermediary level where it consumes Simple Energy, but also can be consumed. This will give it predator-prey relationship with the Dooder agent.

Will be able to observe the evolution of this agent as well.
How it adapts to the Dooder dynamic.
I will also need to give this the ability to continue long into the simulation

> Still in development

## Future Ideas

* Energy creation cycles or periods. Like periods of plenty and scarcity


#### Footnotes
[^1]: https://en.m.wikipedia.org/wiki/Entropy
