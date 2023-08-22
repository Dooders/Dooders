# Cognition

***This page is a work-in-progress*** 

Using the ensemble technique of stacking object specific neural networks, there will be a Meta-Model taking the output of those models as the input to the new model.

For example the Senses module provideds a Dooder its perception of the environment and the energy_detection internal model will be responsible for learning how to detect energy. There will be more internal models like Dooder detection and Hazard detection. Thes low-level models will feed to the meta-model to determine where a Dooder will move in it's step.
