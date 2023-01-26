# Core Components

The core components of the library serve as the foundation for its capabilities. They are designed to be easily and quickly integrated, and follow specific guidelines to provide a solid base for ongoing development and research.

Currently the core components include: [Actions](#Actions), [Steps](#Steps), [Policies](#Policies), [Strategies](#Strategies), [Conditions](#Conditions), and [Collectors](#Collectors).

## Core

The Core class manages the registration of new functions within the existing components.

**Requirements:**

- Every component needs to be available before a simulation starts
- Straightforward usage with decorator based registration
- Consistent and universal schema to store component functions

## Actions

Actions are the primary way an object interacts with the simulation.

***For Example:***  
A Dooder **moves** from one location to another. The action in this case is [move](https://github.com/csmangum/Dooders/blob/main/sdk/actions/move.py).

```python
Action.execute('move', dooder)
```

This command will start the process for a Dooder to move (with default settings, this would be a neural network that learns to find energy)

More information can be found [here]()

## Steps

Steps are the logic a model or object executes during its a cycle.

The step logic will be executed every cycle in the simulation.

***For Example:***  
A Dooder looking for energy, moving to a new location, then ending its turn.

```python
Step.forward('BasicStep', dooder)
```

This command will step a Dooder forward based on the BasicStep logic.

More information can be found [here]()

## Policies

Policies are the way that a model or object makes decisions. In other words, taking information from the environment and making a decision based on that information.

***For Example:***  
There is a movement policy with different options, including a neural network, rule based, and random move.

```python
Policy.execute('NeuralNetwork', dooder)
```

The above command will use the movement policy to create a Neural Network for the Dooder to use to find energy (learning by experience).

More information can be found [here]()

## Strategies

Strategies are a way to get generate fixed or dynamic results, based on the chosen strategy. This can include random numbers, or numbers based on a specific distribution.

The purpose of the strategies is similar to the Policies component but are limited to only being used to support the simulation.

***For example:***  
Generating the number of energy objects to place in the Environment at the beginning of every cycle. That number could be based on a uniform distribution, a normal distribution, or even a static number.

```python
ResourceStrategy = Strategy.load('resources')

strategies = Strategy.compile(ResourceStrategy)
```

The code above loads the resource strategy, and then compiles it to be used in the simulation. The strategy is saved as a file, and then loaded into the simulation.

More information can be found [here]()

## Conditions

The purpose of the Conditions component is to provide a way to check if a specific condition is met, returning if it is True or False. This can be used to check if a Dooder has enough energy to move, or if a Dooder is still alive.

***For example:***
A condition checking if a Dooder should be removed from the simulation. One specific death condition is starvation, where the Dooder has not consumed energy for multiple cycles, and the probability increases with each cycle.

If the condition returns True, the Dooder is removed from the simulation.

```python
result, reason = Condition.check('death', dooder)
```

This code will return weather the condition was met, and the reason why. In this case it could be based on starvation, or another death condition.

More information can be found [here]()

## Collectors

Collectors are function that run every cycle to collect data from objects and models in the simulation. This data can be used to create visualizations, or to analyze the simulation results.

***For example:***
One collects the number of Dooders in the simulation, and another collects the number of energy objects in the simulation.

More information can be found [here]()