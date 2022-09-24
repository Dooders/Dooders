![dooders logo](./docs/dooder_logo.png)
# Dooders
  
 
> Reality works; model it.  
  
  
Dooders is a python library for complex model-based simulations.  

To unpack the terminology a bit:  
* **Complex**: because the library simulates not only a single system, but systems of systems.[^1]  
* **Model-based**: as it includes intersction netween intertwined models. A model is like a map, it's an imperfect and simplified representation of reality.[^2]  
* **Simulation**: because there is power in experimenting with different iterations of a simulation.  

This repo, and the overall project, is a space where I can experiment, learn more about complexity theory and gain a deeper understanding of concepts like feedback loops, attractors, adaptation, etc.. The code, content, and concepts will change over time as I explore different ideas.  

### Primary Goal:
gain an intuition of the mechanics and dynamics of complex systems. The project allows me to have a central location for experimentation and documentation.  

### Primary Strategy:
Complexification[^3] and Integration[^4]. Adding more and more complexity, and imtegration between the evolving models. See how chages affect the simulation and if any emergent[^5] properties surface.  


This project took a lot of inspiration and direction from:

- [Mesa agent-based modeling](https://github.com/projectmesa/mesa)
- [NetLogo](https://github.com/NetLogo/NetLogo)
- [The Romance of Reality](https://www.amazon.com/Romance-Reality-Organizes-Consciousness-Complexity-ebook/dp/B09GW3G45J/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627602&sr=8-2)
- [At Home in the Universe](https://www.amazon.com/At-Home-Universe-Self-Organization-Complexity-ebook/dp/B004VEEO12/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627686&sr=8-1)

## Primary Concepts

| Concept | Explanation |
| ------- | ----------- |
| [**Dooder**](docs/Dooder.md) | An agent object with an amount of 'causal' control in the simulation |  
  

- [**Dooder**](docs/Dooder.md) - An agent object with an amount of causal “control” in the simulation.

- **Experiment** - One or multiple simulations.

- **Simulation** - A full execution of the agent model and additional models (I.e., Environment).

- **Environment** - Proxy for spatial interactions and effects. A lot like a game board.

- **Model** - Analogous to a system. In reality, just about everything is a system. A model serves as a non-object system (non spatial representation).

- **Object** - A model that has a spatial element, like a Dooder or Energy.

- **Energy** - An object that allows a Dooder to perform “work” (execute movements and actions).

- **Cycle** - An iteration of object steps. Given 10 Dooders, 1 cycle would include 10 steps.


## How it works

## Future Plans

| Idea | Description |
| ---- | ----------- |
| Test | Testing 123 |  

## My Background
  
1. BS and MA to be an intelligence analyst
2. Process Improvement
3. Data Science and Ml/Dl
4. Software engineering, fraud detection


[^1]: complexity systems science
[^2]: notes on models
[^3]: Complexification creates conditions for emergent properties. A lot like: "if you complexify it, it will emerge"
[^4]: Adding more and more feedback loops and interfaces inside/between models
[^5]: Emergent properties are properties that only exisit from the imteractions inside/between models. A property that is "greater than the sum of its parts"
