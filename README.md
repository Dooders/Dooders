
# Dooders

![dooders logo](./docs/dooder_logo.png)
  
## Overview

> Reality works; simulate it.  

Systems are anything composed of interacting and dynamic components. For example, Earth's environment is a complex ecological system. A [reef tank](https://www.saltwateraquariumblog.com/9-most-important-reef-tank-aquarium-water-parameters/) is a ever-changing chemical system. Systems can be digital too, like a company's [internal network](https://online.visual-paradigm.com/servlet/editor-content/knowledge/network-diagram/what-is-network-diagram/sites/7/2020/03/network-diagram-example-internal-network-diagram.png). Systems are everywhere.[^1]  

Dooders is a python library for *complex model-based simulations*.  

Unpacking the terminology a bit:  

* **Complex**: The library simulates not only a single system, but systems of systems.[^2]  
* **Model-based**: A model is like a map, it's an imperfect and simplified representation of reality.[^3]  
* **Simulation**: An imitation of a system through a model. Executed to study the behavior.  

This repo, and the overall project, is a space where I can experiment, learn more about complexity theory and gain a deeper understanding of concepts like feedback loops, attractors, adaptation, and a lot more.  

***The code, content, and concepts will change over time as I explore different ideas.***  

### Primary Goal

To gain an intuition of the mechanics and dynamics of complex systems. The project allows me to have a central location for experimentation and documentation.  

### Project Strategy

I will continue to complexify[^4] the library and experiment with more models and observe the interactions inside the simulation. This strategy will help me see how changes affect the results and if any emergent[^5] properties surface.  

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
| Full featured frontend interface | Responsive UI with many dashboards showing the simulation results                                                                  |
| Dockerize deployment             | Make it simple to spin up the entire platform                                                                                      |
| Cognition model                  | Build out the Dooder capability to take in information and evaluate its value                                                      |
| Reproduction model               | Design a function to combine the Genetic models of two Dooders                                                                     |
| Continuous time                  | Switch from step based, to continuous time. Brings on tons of potential issues                                                     |
| Performance                      | Right now I'm focused on function and composition but that will quickly hit the performance wall if I don't optimize at some point |

## My Background

My educational background was aimed towards becoming an intelligence analyst, focusing on remote sensing. After graduate school I needed a job and started at a large insurance company where I discovered the power of data.  

The love of data grew and directed me to python and the world of Data Science. I had a few roles using my Data Science skills in the insurance and financial industry. At the start of the pandemic, I decided to finally go deep into deep learning and neural networks.  

Now, I'm focusing more on software engineering a developing good design principles. This project is the perfect opportunity for me to work on it as I want, and have enough coverage to never get bored.  

## Inspiration

* [Mesa agent-based modeling](https://github.com/projectmesa/mesa)
* [NetLogo](https://github.com/NetLogo/NetLogo)
* [The Romance of Reality](https://www.amazon.com/Romance-Reality-Organizes-Consciousness-Complexity-ebook/dp/B09GW3G45J/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627602&sr=8-2)
* [At Home in the Universe](https://www.amazon.com/At-Home-Universe-Self-Organization-Complexity-ebook/dp/B004VEEO12/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627686&sr=8-1)

## Why?

[A thoughtful and informative explanation](https://media.giphy.com/media/ihvwnO5pHKtyTYQWxU/giphy.gif)  
  
### Footnotes

[^1]: A great book about complex systems is [Thinking in Systems](https://www.amazon.com/Thinking-Systems-Donella-H-Meadows/dp/1603580557/ref=nodl_?dplnkId=c7d91e2b-3d9e-4f2f-b62d-b83301ddb81d)
[^2]: Complex systems have a number of components with non-linear (random or unpredictable) relationships.  
[^3]: In the library, just about everything is separated into models (systems). Functionally that helps a lot, and it helps neatly contain concepts in code.  
[^4]: Complexification creates conditions for emergent properties. Borrowing the slogan from the classic movie *Field of Dreams*: `"if you complexify it, properties will emerge"`  
[^5]: Emergent properties are properties that only exist from the interactions inside/between models. A property that is `"greater than the sum of its parts"`  
