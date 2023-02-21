# Energy

***This page is a work-in-progress***

In this project, energy is a crucial component that enables an agent to persist within the simulation. The Dooder's ability to extract energy from its environment directly impacts its survival. Energy is essential to perform various functions, including movement.

This approach is consistent with the principles of thermodynamics, which have played a significant role in the development of life on Earth[^1]. According to the second law of thermodynamics, systems tend to move towards a state of equilibrium (also known as entropy[^2]) in the absence of an external source of energy, ultimately leading to their demise. This process is similar to how a hurricane gradually loses strength until it dissolves entirely.

A Dooder must utilize energy to avoid thermal equilibrium, which is a terminal state (i.e., death).

## Types of Energy

### Simple Energy: 
Energy that is refreshed each cycle around the environment and can be consumed by all higher level energies.

* Consumed by Dooders and Complex Energy agents
* Allocation is managed by the [Resources](https://github.com/csmangum/Dooders/blob/main/sdk/models/resources.py) class.
* Worth 1 energy unit when consumed.
* Allocation is determined by its [placement strategy](https://github.com/csmangum/Dooders/blob/main/sdk/strategies/placement.py) each cycle (random, etc.).
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
[^1]: [The Romance of Reality](https://www.amazon.com/Romance-Reality-Organizes-Consciousness-Complexity/dp/1637740441/ref=nodl_?dplnkId=7d73a70c-055f-42ff-89cf-05e4a1170b53) beautifully describes how life on Earth likely started and evolved
[^2]: https://en.m.wikipedia.org/wiki/Entropy
