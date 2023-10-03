# SDK Core Components

The core components serve as the foundation for the library and its capabilities. They are designed to be easily and quickly integrated and follow specific guidelines to provide a solid base for ongoing development and research.

Currently, the core components include:

* [Actions](#Actions)
* [Conditions](#Conditions)
* [Policies](#Policies)
* [Steps](#Steps)
* [Strategies](#Strategies)

## Actions

Actions are the primary way an object interacts with the simulation.

***For Example:***  
A Dooder **moves** from one location to another. In this case the action is [`move`](https://github.com/csmangum/Dooders/blob/main/sdk/actions/move.py).

```python
Action.execute('move', dooder)
```

This command will start the process for a Dooder to move (with default settings, the Dooder will learn to search for energy via a neural network model)

> More information on Actions can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Actions.md)

## Conditions

The purpose of the Conditions component is to provide a way to check if a specific condition is met, returning if it is True or False. This can be used to check if a Dooder has enough energy to move, or if a Dooder is still alive, etc..

***For example:***  
[Starvation](https://github.com/csmangum/Dooders/blob/main/sdk/conditions/death.py) is a death condition for a Dooder. If a Dooder has not consumed energy for multiple cycles, the probability of death increases with each cycle it doesn't consume energy.

If the condition returns True, the Dooder is removed from the simulation.

```python
result, reason = Condition.check('death', dooder)
```

This code will check if the condition for death was met, and return the reason why. In this case, it could be based on starvation or another death condition.

> More information on Conditions can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Conditions.md)

## Policies

Policies are the way that a model or object "makes" decisions. A policy takes information from the environment and makes a determination based on its interpertation and evaluation of that information.

***For Example:***  
The [movement](https://github.com/csmangum/Dooders/blob/main/sdk/policies/movement.py) policy offers different options including a neural network, rule-based, and random move to identify where to move in the environment.

```python
Policy.execute('NeuralNetwork', dooder)
```

This code will use the movement policy to create a neural network for the Dooder to learn to find energy (learning by experience). More details on how a Dooder can learn are [here](https://github.com/csmangum/Dooders/blob/main/docs/Learning.md).

> More information on Policies can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Policies.md)

## Steps

Steps are the logic a model or object executes during its cycle. In other words, it's the flow of steps a Dooder will execute each turn.

The step logic will be executed every cycle in the simulation.

***For Example:***  
A Dooder looks for energy, moves to a new location, then ends its turn.

```python
Step.forward('BasicStep', dooder)
```

This command will step a Dooder forward based on the [BasicStep](https://github.com/csmangum/Dooders/blob/main/sdk/steps/dooder.py) logic. This logic can vary based on user settings, but currently, the default is a neural network.

> More information on Steps can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Steps.md)

## Strategies

Strategies are a way to get generate fixed or dynamic results, based on the chosen strategy. This can include random numbers or numbers based on a specific distribution.

The purpose of the strategies is similar to the Policies component but is limited to only being used to support the simulation.

***For example:***  
Generating the number of energy objects to place in the Environment at the beginning of every cycle. That number could be based on a uniform distribution, a normal distribution, or even a static number.

```python
ResourceStrategy = Strategy.load('resources')

strategies = Strategy.compile(ResourceStrategy)
```

The code above loads the resource strategy, and then compiles it to be used in the simulation. The strategy is saved as a file and then loaded into the simulation. In this case, the result could be the number of new energy objects = 20.

> More information on Strategies can be found [here](https://github.com/csmangum/Dooders/blob/main/docs/Strategies.md)
