# Learning

A main objective of the project is to explore the learning capabilities of Dooders within the environment. This requires systematic experimentation to evaluate various strategies and approaches for the Dooder to gather information from the simulation and apply it towards increasing its longevity.

In essence, the Dooder agent will exhibit learning through its exposure and interpretation of the simulated environment. It will learn through its own unique perspective and experience.

## Mind Models

A Mind, in the library, is a model for the way the Dooder experiences and behaves in the simulation, how it perceives the environment, and how it reacts to it. A Dooder's mind model is a representation of its cognitive process.

The model is activated each step for every Dooder in the Environment.

### Example

Here is one example of a mind model that takes a literal interpretation of the process during a Dooder's step.

![Mind Model Example](/docs/images/mind_model_example.jpg)

[Perception](/docs/Perception.md) is a Dooder's capability to comprehend its environment and gather information in the simulation. However, this perception is limited and only provides a restricted viewpoint of the Dooder's surroundings. 

[Perspective](/docs/Perspective.md), coming from a Dooder's perception, is a dynamic interpretation of the Dooder's environment that is shaped by its outlook and goals. This perspective can change as the Dooder's outlook and goals evolve.

[Intuition](/docs/Intuition.md) acts as a sort of fast-access memory for the Dooder, used in situations where cognition is not allowed or necessary. Like a reflex, the Dooder can rely on intuition to take action without the need for processing during its turn. 

[Cognition](/docs/Cognition.md) is the Dooder's ability to process information and make decisions, adapting to its environment through its ability to think. This is how a Dooder will learn.

In the Dooder's mind model, the primary outcome of each step is a choice of action, updated short-term goals, and an updated outlook of the future. The outlook is similar to the concept of mood. If a Dooder is not allowed to think, it will act solely based on intuition, and only its choice of action will be updated.

Research is currently focused on using neural networks as a key component of the Dooder's mind model, with other approaches coming later.

### Neural Networks

The default design uses a straightforward [neural network](https://github.com/csmangum/Dooders/blob/main/sdk/learning/nets/model.py) with back-propagation. The weights and biases in the neural network serve as a genetic memory, recording information over successive iterations that are directly inaccessible to the Dooder. However, the weights can be modified based on the experiences and decisions made by the Dooder (model training).

The weights that `fit` closest to the simulation dynamics will persist through generations of Dooders.

Example implementation: [movement policy](/dooders/sdk/policies/movement.py)

### Future Research

* Bayesian Neural Networks
* Feed-Forward Neural Networks
* Reinforcement Learning
* Graph Neural Networks
* Hierarchical Learning


