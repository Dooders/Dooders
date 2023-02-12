# Dooder

***This page is a work-in-progress***

A Dooder is the primary agent object in the [simulation](Simulation.md). An agent is defined as an entity that has causal power, in other words, it has the ability to interact with its environment.[^1]

Another way of thinking about it is an agent can take in information and use that to increase its survivability. Naturally, an agent's causal power increases as its ability to evaluate information also increases.[^2]  

### Laws

A law is an aspect of the simulation the Dooder cannot control.

- A Dooder executes a step function every cycle
- A Dooder will progress step after step until it reaches a terminal state (death)
- A step has a specific phases of execution (React, Move, Act)
- Each cycle without consuming Energy will add to it's hunger state, increasing the chance of starvation

## Step Phases

- During the React phase, a Dooder will resolve any debts to the simulation
  - A debt is a situation that affects a Dooder while outside the Dooder's turn
- During the Move phase, a Dooder can relocate to a new location
- During the Act phase, a Dooder can execute more intentional actions
- The React phase is restricted to simple and quick actions, while the Act phase allows for more complex actions
- A Dooder needs Energy to survive

## Energy

The [Environment](Environment.md) model is responsible for managing any object that has a spatial component like a Dooder or Energy object. These objects move to different locations within a grid and interact with each other.  

[Energy](Energy.md) is the primary resource a Dooder has to interact in the environment. Every action will have a cost and energy will be allocated to the environment every cycle.  

The [Resources](Resources.md) model will manage the allocation of energy to the environment. Following a user defined strategy.  

The current strategy is to randomly select locations in the environment and place a variable number of energy units for Dooder's to consume. Each Dooder gets a Genetics defined starting energy level, max energy supply, and energy consumption rate.  

## Genetics and Behavior

The initial seed population is generated based on the selected genetic attributes and the strategies to populate the attributes. The [Genetics](Genetics.md) model serves as a way to establish starting values that can be mutable or immutable.  

For example, the starting energy value is determined at Dooder creation as the `energy_supply` attribute and changes cycle to cycle. Permanent values might be something like Metabolism which defines the rate a Dooder will starve with no new energy.  

A Dooder's behavior is an expression of both its genetics and environment. Some attributes can change over time, like the energy supply, while others can be immutable, like the metabolism. 


## Death and Reproduction

A Dooder agent will continue as long as it meets defined conditions (or states). For example, hunger is represented by a function that will keep track of the number of cycles with `energy_supply = 0`.  

Dooder reproduction is still in the works after the base functionality is in the library.  


### Footnotes

[^1]: Put in reference  
[^2]: Put in reference  
