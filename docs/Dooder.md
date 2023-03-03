# Dooder

***This page is a work-in-progress***

A Dooder is the primary agent object in the [simulation](Simulation.md). An agent is an object that has `causal power` and the ability to interact with its environment.

An agent can take in information and use that to increase its survivability. Naturally, an agent's causal power increases as its ability to evaluate information also increases.

## Rules

A rule is an aspect of the simulation the Dooder cannot control or influence.

- A Dooder executes one Step every cycle
- A Dooder will continue step after step until it reaches a terminal state (death)
- Every Dooder will execute a step during a cycle before the next cycle can start
- A step has specific phases of execution (React, Move, Act)
- A Dooder’s hunger state will increase every consecutive cycle without energy; increasing the chance of starvation

#### For more explanations:
- How a Dooder will [learn](https://github.com/csmangum/Dooders/blob/main/docs/Learning.md)
- How it will [percieve](https://github.com/csmangum/Dooders/blob/main/docs/Perception.md) its surroundings

---


## Genetics and Behavior

The initial seed population is generated based on the selected genetic attributes and the strategies to populate the attributes. The [Genetics](Genetics.md) model serves as a way to establish starting values that can be mutable or immutable.  

For example, the starting energy value is determined at Dooder creation as the `energy_supply` attribute and changes cycle to cycle. Permanent values might be something like Metabolism which defines the rate a Dooder will starve with no new energy.  

A Dooder's behavior is an expression of both its genetics and environment. Some attributes can change over time, like the energy supply, while others can be immutable, like the metabolism. 


## Death and Reproduction

A Dooder agent will continue as long as it meets defined conditions (or states). For example, hunger is represented by a function that will keep track of the number of cycles with `energy_supply = 0`.  

Dooder reproduction is still in the works after the base functionality is in the library.  
