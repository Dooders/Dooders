# Development Diary

A space to log what I've been working in and thinking. That will help look back and remember why I made certain decisions or chose to take a specific path.

Sorted by the most recent entry

---

## 2023-01-01 Metrics

I finished up with some of the metrics to be collected at each cycle. I will need to improve the way a model is added to do the cycle collection and reset attributes after.

I've also been thinking of specific experiment scenarios I might want to have written where I want to answer specific questions (Does the simulation plateau?, etc). This could make experiment assessment a lot more descriptive and valuable.

## 2022-12-23 Foresight, Perception, and Perspective

I've been thinking over a few future ideas that I want look into at some point. Thinking about how the Dooder interacts in the simulation.

First is Foresight. Adding functionality that allows a Dooder to use past experience to predict the future. This would be a way to improve the Dooder's ability to make decisions. It would also be a way to improve the Dooder's ability to learn.

Second is Perception. Adding functionality that allows a Dooder to perceive the environment. Essentially, it's how much data (Information) the Dooder can "consume" from the environment. There is a lot of data and noise, so a Dooder can only perceive a small amount of it. But that amount can grow.

The third is Perspective. Perspective would work like a lense. The particular perception influences how a Dooder evaluates it's perception. So, information the Dooder collects can be evaluated differently based on a "perspective"; that I still need to work out. Perspective would be influence by a whole host of factors.

## 2022-12-19 BaseStats

Created the BaseStats class to better manage agent creation and creation of necessary attributes. I've worked out what I want at the individual Dooder level, next will be simulation level, then society level.

Building out the data that I want to see from each perspective.

## 2022-12-16 Actions done

Finished the Actions class buildout. Also had to refactor some other classes to make it wall work. Next step might be working on the data/metric side of things. I want a better way to collect data from the simulation, and improve the specific data that I want to see.  

## 2022-12-13 Actions, Policies, and Models

Working through my current goal to better handle the internal models. I've mostly worked out the Action class will register all possible actions and handle the execution of an action, like Move or Reproduce.

Actions will contain policies that determine how the action behaves. Models are one way to learn and interact with the environment.

Next step is to start building that out.

## 2022-12-11 InternalModels fix

I discovered a bug where the models are only created when called the first time. I need to make it so all simulation actions have the required models loaded first. I noticed the bug when testing if the weights of parent Dooders are combined with the different policies.

## 2022-12-08 Actions and Step Phases

Next step on the design updates is to build out an Action class to manage all the different actions possible in the simulation. At first will there will only be the consume, move and reproduce actions.

Secondly, taking a "phase" approach to the Dooder step functions. It will be React, Move, Act (in that order). React will be to resolve any "debts" to the simulation, in other words, any situations that affect a Dooder while outside the Dooder's turn, must be resolved first.

The Move phase will allow the Dooder to improve it's situation by moving to another Location, or it can decide not to move. The Act phase will contain all the more planned/inferred actions the Dooder will take. This phase allows more "thinking" where the React phase restricts actions that are much simpler and rule-like.  

## 2022-12-07: InternalModels class

I finished up the InternalModels class. It's a dictionary-like class that holds the internal models for each Dooder. It allows for easy access to the weights and biases of the NeuralNetworks. It also allows for easy access to the models themselves.  

## 2022-12-05 Building out the Dooder step process

I'm first going to create a custom dictionary class to handle the internal models. That way I can easily access the weights and biases of every model.  

Then I'm going to update the movement policy to be goal-based. The goal will be inferred by the Dooder's state.  

## 2022-12-04: Managing multiple learning models

Right now I'm working out the best design to manage multiple learning models. Currently a Dooder only has a model to determine where to move (saved as a class attribute called internal_models). I'll be adding many more models going further so I need a consistent design.  

A simple dictionary may be enough, but I want to think through it a bit more before taking that route.

I'm also thinking about better ways to "collect" data during a simulation. Something that can be easily changed to collect the specific data I want. I'll be adding a lot of data-points to the simulation and I want to be able to easily change what data is collected.  
