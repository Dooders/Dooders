# Movement Policy

Develop and test different movement policies available to a Dooder. A movement policy provides a decision point on what a Dooder will do next. Currently, the goal is to find more energy to consume, to prolong its life.

## Goals

- [x] Create a movement system that allows the Dooder to move in 1 of 9 directions (includes the current position)
- [x] Develop and test three movement policies (Random, Rule-based and Simple Neural Network)
- [x] Determine which policy maximizes Energy consumption, a Dooder's lifespan, and it's ability to learn

## Requirements

- Input: The Dooder object which will have the current position and details about its neighboring locations
- Output: The recommended position a Dooder should move to
- Action: The Dooder will move to the recommended position and consume Energy, if there is any

## Plan

1. Create a Policy class to register and manage the different movement policies
2. Create each Movement policy
3. Adapt Dooder class to use the Movement policy

## Details

### RandomMove

This policy will take a list of all adjacent locations and will choose a random location

### RuleBased

This policy will identify all neighboring objects and creates a list of locations with energy. Then a random location is chosen, if there are no neighboring energy objects, the Dooder will not move.

### Simple Artificial Neural Network

This policy will use a simple ANN to determine the best location to move to. The model, for the time being, will have 9 inputs (one for each location) and 9 outputs (one for each location). The neural network will need to select the best option, and will learn over its lifetime.

## Results

Current energy allocation strategy is a random number of energy objects, placed randomly in the environment. The Dooder will consume energy if it is in the same location as an energy object. The Dooder will also consume energy if it moves to a location with an energy object.

I ran 10,000 simulations for each movement policy. The results are as follows:

| Metric                     | RandomMove | RuleBased | SimpleNeuralNetwork |
| -------------------------- | ---------- | --------- | ------------------- |
| **Mean Cycle Count**       | 22.33      | 99.74     | 66.02               |
| **Median Cycle Count**     | 21.00      | 100.00    | 67.00               |
| **Mean Energy Consumed**   | 18.28      | 380.17    | 72.21               |
| **Median Energy Consumed** | 17.00      | 382.00    | 69.00               |

Not surprisingly, the RuleBased policy performed the best. That's because it will always choose a location with energy. The RandomMove policy is a good benchmark for an agent with zero "intelligence". The RuleBased is also not representative of an intelligent agent.

The NeuralNetwork policy is the best choice for a policy that allows for a Dooder to learn, and apply that to the environment. It also allows for learning from new conditions, which RuleBased does not allow.

## Next Steps

- Work on a Reproduction Policy
- Develop more Movement Policies. Leveraging Reinforcement Learning and other decision making strategies
