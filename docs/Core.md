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


## Conditions


## Collectors

