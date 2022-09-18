# Dooders

Dooders is a python library for complex model-based simulation.

This repo, and the overall project, is a space where I can experiment and learn more about complexity theory. The code, content, and concepts will change over time as I explore different ideas.

My primary goal is to gain an intuition of the mechanics of complex systems. The project allows me to have a central location for experimentation and documentation. GitHub also provides the added value of branches and version control.

This project took a lot of inspiration and direction from:

- [Mesa agent-based modeling](https://github.com/projectmesa/mesa)
- [NetLogo](https://github.com/NetLogo/NetLogo)
- [The Romance of Reality](https://www.amazon.com/Romance-Reality-Organizes-Consciousness-Complexity-ebook/dp/B09GW3G45J/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627602&sr=8-2)
- [At Home in the Universe](https://www.amazon.com/At-Home-Universe-Self-Organization-Complexity-ebook/dp/B004VEEO12/ref=tmm_kin_swatch_0?_encoding=UTF8&qid=1661627686&sr=8-1)

## Primary Concepts

- [**Dooder**](docs/Dooder.md) - An agent object with an amount of causal “control” in the simulation.

- **Experiment** - One or multiple simulations.

- **Simulation** - A full execution of the agent model and additional components (I.e., Environment).

- **Environment** - Proxy for spatial interactions and effects. A lot like a game board.

- **Model** - Analogous to a system. In reality, just about everything is a system. A model serves as a non-object system (non spatial representation).

- **Object** - A model that has a spatial element, like a Dooder or Energy.

- **Energy** - An object that allows a Dooder to perform “work” (execute movements and actions).

- **Cycle** - An iteration of object steps. Given 10 Dooders, 1 cycle would include 10 steps.




This is an example of how I can do a footnote. [^fn]


[^fn] And this his how I would cite it.

