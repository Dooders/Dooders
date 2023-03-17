# Dooder

***This page is a work-in-progress***

A Dooder is the primary agent object in the [simulation](Simulation.md). An agent is an object that has causal power and the ability to interact with its environment.

An agent can take in information and use that to increase its survivability. Naturally, an agent's causal power increases as its ability to evaluate information also increases.

## Rules

A rule is an aspect of the simulation the Dooder cannot control or influence.

- A Dooder executes one Step every cycle
- A Dooder will continue step after step until it reaches a terminal state (death)
- Every Dooder will execute a step during a cycle before the next cycle can start
- A step has specific phases of execution (React, Move, Act)
- A Dooder’s hunger state will increase every consecutive cycle without energy; increasing the chance of starvation
- A Dooder can alter the environment and interact in the simulation

## FAQ
- How will a Dooder [learn](https://github.com/csmangum/Dooders/blob/main/docs/Learning.md)?
- How can a Dooder [percieve](https://github.com/csmangum/Dooders/blob/main/docs/Perception.md) its surroundings?

## Data
