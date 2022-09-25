
# Dooders

![dooders logo](./docs/dooder_logo.png)
  
> Reality works; model it.  

## Overview

Dooders is a python library for *complex model-based simulations*.  

Unpacking the terminology a bit:  

* **Complex**: The library simulates not only a single system, but systems of systems.[^1]  
* **Model-based**: A model is like a map, it's an imperfect and simplified representation of reality.[^2]  
* **Simulation**: Continual experimentation and observing of models.  

This repo, and the overall project, is a space where I can experiment, learn more about complexity theory and gain a deeper understanding of concepts like feedback loops, attractors, and adaptation.  

***The code, content, and concepts will change over time as I explore different ideas.***  


### Primary Goal

To gain an intuition of the mechanics and dynamics of complex systems. The project allows me to have a central location for experimentation and documentation.  

### Primary Strategy

Ongoing complexification[^3] and integration[^4]. See how changes affect the simulation and if any emergent[^5] properties surface.  

### Primary Concepts

| Concept                                | Explanation                                                                      |
| :------------------------------------- | -------------------------------------------------------------------------------- |
| [**Dooder**](docs/Dooder.md)           | An agent object with an amount of causal 'control' in the simulation             |
| [**Model**](docs/Model.md)             | Analogous to a system. In reality, just about everything is a system of some kind           |
| [**Simulation**](docs/Simulation.md)   | A full execution of the agent model and additional models (I.e., Environment, Society)    |
| [**Experiment**](docs/Experiment.md)   | One or multiple simulations                                                      |
| [**Environment**](docs/Environment.md) | Proxy for spatial interactions and effects. A lot like a game board              |
| [**Energy**](docs/Energy.md)           | An object that allows a Dooder to perform “work” (execute movements and actions) |
| [**Cycle**](docs/Cycle.md)             | An iteration of object steps. Given 10 Dooders, 1 cycle would include 10 steps   |
  
  
## How it works
  
  

## Future Plans

| Idea | Description |
| ---- | ----------- |
| Full featured frontend interface | |
| Dockerized deployment | |
| Cognition model | |
| Reproduction model | |  

## My Background
  
1. BS in Geospatial Intelligence and a Master's in National Security Studies
   * I was planning on being an intelligence analyst focusing on satellite imagery
2. Process Improvement
    * Needed a job after grad-school, that introduced me to the idea of process improvement. Learned a lot about the types of waste, inefficiencies, and the value of data
3. Data Science with Machine Learning and Deep Learning
    * Loved the idea of using data to make predictions and decisions. I had roles in different industries looking to identify patterns and trends in data
4. Software engineering, fraud detection
    * My current role is a mix of many different roles. I am now more focused on creating systems and process and better ways to catch undetected financial fraud


## Inspiration

* [Mesa agent-based modeling](https://github.com/projectmesa/mesa)
* [NetLogo](https://github.com/NetLogo/NetLogo)
* [The Romance of Reality](https://www.amazon.com/Romance-Reality-Organizes-Consciousness-Complexity-ebook/dp/B09GW3G45J/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627602&sr=8-2)
* [At Home in the Universe](https://www.amazon.com/At-Home-Universe-Self-Organization-Complexity-ebook/dp/B004VEEO12/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627686&sr=8-1)


## Why?

[A thoughtful and informative answer](https://media.giphy.com/media/ihvwnO5pHKtyTYQWxU/giphy.gif)  
  
  
# Footnotes

[^1]: complexity systems science  
[^2]: notes on models  
[^3]: Complexification creates conditions for emergent properties. A lot like: "if you complexify it, it will emerge"  
[^4]: Adding more and more feedback loops and interfaces inside/between models  
[^5]: Emergent properties are properties that only exist from the interactions inside/between models. A property that is "greater than the sum of its parts"  
