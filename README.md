
# Dooders

![dooders logo](./docs/dooder_logo.png)
  
## Overview

> Reality works; simulate it.  

Systems are anything composed of interacting and dynamic components. For example, Earth's environment is a complex ecological system. A [reef tank](https://www.saltwateraquariumblog.com/9-most-important-reef-tank-aquarium-water-parameters/) is a ever-changing chemical system. Systems can be digital too, like a company's [internal network](https://online.visual-paradigm.com/servlet/editor-content/knowledge/network-diagram/what-is-network-diagram/sites/7/2020/03/network-diagram-example-internal-network-diagram.png). Systems are everywhere.[^1]  

Dooders is a python library for *complex model-based simulations*.  

Unpacking the terminology a bit:  

* **Complex**: The library simulates not only a single system, but systems of systems.[^2]  
* **Model-based**: A model is like a map, it's an imperfect and simplified representation of reality.
* **Simulation**: An imitation of a system through a model. Executed to study the behavior.  

This repo, and the overall project, is a space where I can experiment, learn more about complexity theory and gain a deeper understanding of concepts like feedback loops, attractors, adaptation, and a lot more.  

***The code, content, and concepts will change over time as I explore different ideas.***  

### Main Concepts

| Concept                                | Explanation                                                                            |
| :------------------------------------- | -------------------------------------------------------------------------------------- |
| [**Dooder**](docs/Dooder.md)           | An agent object with an amount of causal 'control' in the simulation                   |
| [**Model**](docs/Concepts.md#Model)    | Analogous to a system. In reality, just about everything is a system of some kind      |
| [**Simulation**](docs/Simulation.md)   | A full execution of the agent model and additional models (I.e., Environment, Society) |
| [**Experiment**](docs/Experiment.md)   | One or multiple simulations                                                            |
| [**Environment**](docs/Environment.md) | Proxy for spatial interactions and effects. A lot like a game board                    |
| [**Energy**](docs/Energy.md)           | An object that allows a Dooder to perform “work” (execute movements and actions)       |
| [**Cycle**](docs/Concepts.md)          | An iteration of object steps. Given 10 Dooders, 1 cycle would include 10 steps         |
  
## How it works

   > TBD
  
## Future Plans

| Idea                             | Description                                                                                                                        |
| :------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Full featured interface | Responsive UI with many dashboards showing the simulation results                                                                  |
| Dockerize deployment             | Make it simple to spin up the entire platform                                                                                      |
| [Cognition model](https://github.com/csmangum/Dooders/blob/main/docs/plans/CognitionModel.md)                | Build out the Dooder capability to take in information and evaluate its value                                                      |
| Reproduction model               | Design a function to combine the Genetic models of two Dooders                                                                     |
| Continuous time                  | Switch from step based, to continuous time. Brings on tons of potential issues                                                     |
| Performance & Efficiency                   | Right now I'm focused on function and composition but that will quickly hit the performance wall if I don't optimize at some point |
| Simulation parameters | Make it so simulation strategies and parameters can be changed easily |
| Senses model | Right now a Dooder has no way to aquire information that isn't directly fed to it. A senses model allows a Dooder to aquire information from the environment |

## Why?

[A thoughtful and informative explanation](https://media.giphy.com/media/ihvwnO5pHKtyTYQWxU/giphy.gif)  (A better [answer](https://rememberization.substack.com/p/why-dooders))

## Links

  
### Footnotes

[^1]: A great book about complex systems is [Thinking in Systems](https://www.amazon.com/Thinking-Systems-Donella-H-Meadows/dp/1603580557/ref=nodl_?dplnkId=c7d91e2b-3d9e-4f2f-b62d-b83301ddb81d)
[^2]: Complex systems have a number of components with non-linear (random or unpredictable) relationships.  
