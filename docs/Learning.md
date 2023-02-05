# Learning

A main objective of the project is to explore the learning capabilities of Dooders within the environment. This requires systematic experimentation to evaluate various strategies and approaches for the Dooder to gather information from the simulation and apply it towards increasing its longevity.

In essence, the Dooder agent will exhibit learning through its exposure and interpretation of the simulated environment.

## Mind Models

A mind is a model for the way the Dooder experiences and acts in the simulation, how it perceives the environment, and how it reacts to it. A Dooder's mind model is a representation of its cognitive process in the simulation.

### Example

Here is one example of a mind model that takes a literal interpretation of the process during a Dooder's step.

![Mind Model Example](/docs/images/mind_model_example.jpg)

[Perception](/docs/Perception.md) is a Dooder's capability to comprehend its environment and gather information in the simulation. However, this perception is limited and only provides a restricted viewpoint of the Dooder's surroundings. 

[Perspective](/docs/Perspective.md), coming from a Dooder's perception, is a dynamic interpretation of the Dooder's environment that is shaped by its outlook and goals. This perspective can change as the Dooder's outlook and goals evolve.

[Intuition](/docs/Intuition.md) acts as a sort of fast-access memory for the Dooder, used in situations where cognition is not allowed. Like a reflex, the Dooder can rely on intuition to take action without the need for processing during its turn. Cognition is the Dooder's ability to process information and make decisions, adapting to its environment through its ability to think.

In the Dooder's mind model, the primary outcome of each step is a choice of action, updated short-term goals, and an updated outlook of the future. The outlook is similar to the concept of mood. If a Dooder is not allowed to think, it will act solely based on intuition, and only its choice of action will be updated.

Research is currently focused on using neural networks as a key component of the Dooder's mind model.

### Neural Networks

A cognitive and intuitive design approach, utilizing a straightforward neural network with back-propagation, is being utilized to direct the movements of a Dooder towards a target, such as Energy or another Dooder. The weights and biases in the neural network serve as a genetic memory, recording information over successive iterations that are directly inaccessible to the Dooder. However, the weights can be modified based on the experiences and decisions made by the Dooder (model training).

### Future Research

* Bayesian Neural Networks
* Feed-Forward Neural Networks
* Reinforcement Learning
* Graph Neural Networks
