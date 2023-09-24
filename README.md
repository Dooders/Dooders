
# Dooders

![dooders logo](./docs/dooder_logo.png)

> Reality works; simulate it.  
  
## Overview

Dooders is an open-source research project focused on the development of artificial intelligent agents in a simulated reality. The project aims to enable the conditions and mechanisms for cognitive agents to evolve and emerge in a digital environment.

A [Dooder](docs/Dooder.md) is an agent object in the simulation with an amount of causal control. It acts in the simulation only as long as it consumes [Energy](https://github.com/csmangum/Dooders/blob/main/docs/Energy.md).

Take a look on how a Dooder will [learn and act](https://github.com/csmangum/Dooders/blob/main/docs/Learning.md), get an overview of the [core components](https://github.com/csmangum/Dooders/blob/main/docs/Core.md) of the library, or read [why I started the project](https://github.com/csmangum/Dooders/blob/main/docs/Why.md).

I will also be documenting experiments in [substack](https://rememberization.substack.com/p/experiment-list). Including the results from my [first experiment](https://rememberization.substack.com/p/experiment-1-single-simulation).

***The code, content, and concepts will change over time as I explore different ideas.***  

***Everything in this repository should be considered unfinished and a work-in-progress***
  
### How to use it

```python
from dooders import Experiment

experiment = Experiment()

experiment.simulate()

experiment.experiment_summary()


# Example output using the default settings
# This simulation ended after 53 cycle when 
# all Dooders died from starvation

{'SimulationID': 'XGZBhzoc8juERXpZjLZMPR',
 'Timestamp': '2023-03-09, 18:20:33',
 'CycleCount': 53,
 'TotalEnergy': 634,
 'ConsumedEnergy': 41,
 'StartingDooderCount': 10,
 'EndingDooderCount': 0,
 'ElapsedSeconds': 0,
 'AverageAge': 14}
```
For more details, see the [Quick Start guide](docs/QuickStart.md).  


