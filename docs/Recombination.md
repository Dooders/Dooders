## Crossover

Inspired by the genetic recombination process seen in nature, this technique selects a random crossover point within the layer weights of the two parent Dooders. We then construct the offspring's layer weights by combining the weights from parent #1 to the left of the crossover point and the weights from parent #2 to the right of the crossover point. This mimics the genetic shuffling observed during sexual reproduction, introducing variation into the offspring population.

```python
# With a random crossover point of 3
parent_1 = [.1, .2, .3, .4, .5]
parent_2 = [.6, .7, .8, .9, .1]

offspring = [.1, .2, .3, .9, .1]
```

## Lottery

In the random approach, the offspring's weights are determined by a simple lottery system. Each weight is chosen randomly from either parent #1 or parent #2. This method introduces an additional element of randomness into the generation of the next set of Dooders, enhancing the chances of discovering novel and potentially beneficial configurations of weights.

```python
parent_1 = [.1, .2, .3, .4, .5]
parent_2 = [.6, .7, .8, .9, .1]

offspring = [.1, .2, .8, .9, .5]
```

## Averaging

The average methodology takes a more conservative route to recombination. Rather than leaning heavily on either parent, this approach generates the offspring's weights by taking the average of corresponding weights from parent #1 and parent #2. This method ensures a smoother transition from one generation to the next, encouraging the incremental refinement of successful weight configurations while still introducing some degree of variation.

```python
parent_1 = [.1, .2, .3, .4, .5]
parent_2 = [.6, .7, .8, .9, .1]

offspring = [.35, .45, .55, .65, .30]
```

## Random Range

Lastly, the random range method operates on a principle of random selection within established limits. Here, each weight for the offspring is chosen as a random value that falls within the range of the corresponding weights of parent #1 and parent #2. This approach maintains the extent of variation exhibited by the parents, but allows for the offspring to explore unique weight combinations that might not have been present in either parent.

## Blend

In the blend methodology, a random convex combination of the parent weights is used. The offspring weights are calculated as αw1 + (1-α)w2 where w1 and w2 are weights from parent 1 and parent 2 respectively, and α is a random number between 0 and 1. This method allows the exploration of the space between the parents' weights and could result in offspring with performance characteristics that blend those of their parents.

## Elitism

Elitism is a strategy where the best performing individuals from a population are selected to pass on their traits to the next generation without undergoing recombination or mutation. This guarantees the survival of the best performing weights and biases, ensuring the evolutionary progress made does not regress. The offspring are then generated from the remaining population using other recombination methodologies.

## Uniform Crossover

A variation of the crossover methodology is the uniform crossover. In this method, each weight for the offspring is chosen from either parent with equal probability. This is similar to the random approach but restricts the randomness to two specific points – the corresponding weights of the two parents.

## Heuristic Crossover

In this methodology, one parent is selected as the "better" one based on some fitness criterion. The offspring weights are then created by a combination of the better parent's weights and the difference between the two parents' weights. This allows the offspring to explore the space in the direction from the worse to the better parent, which could potentially lead to better solutions.

## Simulated Binary Crossover (SBX)

SBX is a recombination method that tries to simulate the behavior of one-point, two-point, and uniform crossover for binary strings in the context of real-valued strings. It's an excellent choice when you want to maintain diversity in the population and can help avoid premature convergence to a suboptimal solution.

## Single Active Crossover

This method requires a bit more information about the structure of the neural network. It identifies the most "active" neuron (or layer) — the one that, when modified, would most change the network's output — and passes that active neuron (or layer) to the offspring. This method could be useful in cases where certain parts of the network have proven particularly effective and should be preferentially preserved.

## Convolutional Crossover

For networks that utilize convolutional layers, a crossover method that preserves the spatial relationships within those layers may be useful. In convolutional crossover, blocks of neurons that correspond to the same spatial location in the parent networks are kept together in the offspring network. This could be helpful for tasks like image recognition, where spatial relationships between features are important.
