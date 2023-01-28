# Core Components

The core components serve as the foundation for the library and its capabilities. They are designed to be easily and quickly integrated, and follow specific guidelines to provide a solid base for ongoing development and research.

Currently the core components include: [Actions](#Actions), [Steps](#Steps), [Policies](#Policies), [Strategies](#Strategies), [Conditions](#Conditions), and [Collectors](#Collectors).

## Actions

Actions are the primary way an object interacts with the simulation.

***For Example:***  
A Dooder **moves** from one location to another. The action in this case is [move](https://github.com/csmangum/Dooders/blob/main/sdk/actions/move.py).

```python
Action.execute('move', dooder)
```

This command will start the process for a Dooder to move (with default settings, the dooder will learn to search for energy via a neural network)

More information on Actions can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Actions.md)

## Steps

Steps are the logic a model or object executes during its a cycle. In other words, it's the flow of steps a dooder will execute each turn.

The step logic will be executed every cycle in the simulation.

***For Example:***  
A Dooder looking for energy, moving to a new location, then ending its turn.

```python
Step.forward('BasicStep', dooder)
```

This command will step a Dooder forward based on the [BasicStep]() logic. This logic can vary based on user settings, but currently the default is a neural network.

More information on Steps can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Steps.md)

## Policies

Policies are the way that a model or object "makes" decisions. A policy takes information from the environment and makes a determination based on interpertation and evaluation of that information.

***For Example:***  
The [movement]() policy offers different options including: a neural network, rule based, and random move.

```python
Policy.execute('NeuralNetwork', dooder)
```

This code will use the movement policy to create a neural network for the Dooder to learn to find energy (learning by experience). More details on how a dooder can learn is [here]().

More information on Policies can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Policies.md)

## Strategies

Strategies are a way to get generate fixed or dynamic results, based on the chosen strategy. This can include random numbers, or numbers based on a specific distribution.

The purpose of the strategies is similar to the Policies component but are limited to only being used to support the simulation.

***For example:***  
Generating the number of energy objects to place in the Environment at the beginning of every cycle. That number could be based on a uniform distribution, a normal distribution, or even a static number.

```python
ResourceStrategy = Strategy.load('resources')

strategies = Strategy.compile(ResourceStrategy)
```

The code above loads the resource strategy, and then compiles it to be used in the simulation. The strategy is saved as a file, and then loaded into the simulation. In this case, the result could be the number of new energy objects = 20.

More information on Strategies can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Strategies.md)

## Conditions

The purpose of the Conditions component is to provide a way to check if a specific condition is met, returning if it is True or False. This can be used to check if a Dooder has enough energy to move, or if a Dooder is still alive, etc..

***For example:***
[Starvation]() is a death condition for a Dooder. If a Dooder has not consumed energy for multiple cycles, the probability of death increases with each cycle it doesn't consume energy.

If the condition returns True, the Dooder is removed from the simulation.

```python
result, reason = Condition.check('death', dooder)
```

This code will check if the condition for death was met, and and return the reason why. In this case it could be based on starvation, or another death condition.

More information on Conditions can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Conditions.md)

## Collectors

Collectors are functions that run every cycle to collect data from objects and models in the simulation. This data can be used to create visualizations, or to analyze the simulation results.

***For example:***
Each model or object has a number of collectors. One example is a collector that keeps track of the number of energy objects in the Environment.

More information on Collectors can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Collectors.md)
