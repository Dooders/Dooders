# Dooder

A Dooder is the primary agent object in the [simulation](Simulation.md). An agent is defined as an entity that has causal power, or has the ability to interact with its environment.[^1]

Another way of thinking about it is an agent can take in information and use that to increase its survivability. Naturally, an agent's causal power increases as its ability to evaluate information also increases.[^2]


A Dooder contains the following sub models:  

- [Behavior](Behavior.md)
- [Cognition](Cognition.md)
- [Genetics](Genetics.md)


A Dooder is also a component of higher level models like:  

- [Environment](Environment.md)
- [Society](Society.md)
- [Information](Information.md)


## How will Dooders use energy?

Energy is the primary resource a Dooder has to interact in the environment. Every action will have a cost and energy will be allocated to the environment every cycle.

The Resource model will manage the allocation of energy to the environment. Following a user defined strategy.

The current strategy is to randomly select locations in the environment and place a variable number of energy units for Dooder's to consume. Each Dooder gets a Genetics defined starting energy level, max energy supply, and energy consumption rate.



## Genetics and Behavior





[^1]: Put in reference
[^2]: Put in reference
