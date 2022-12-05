""" 
The movement policy is responsible for "deciding" where a Dooder will move during it's step
Currently there are three policies:
1. Random: The Dooder will move to a random location
2. Rule-based: The Dooder will move to a location based on a set of rules
3. Neural Network: The Dooder will move to a location based on a neural network output
"""

from random import choice
from typing import TYPE_CHECKING

import numpy as np

from sdk.learning.nets.model import SimpleNeuralNet
from sdk.base.base_policy import BasePolicy
from sdk.core.policies import Policies

if TYPE_CHECKING:
    from sdk.models.dooder import Dooder


@Policies.register()
class RandomMove(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood
    A neighborhood is all surrounding positions, including the current position

    Args:
        dooder: The Dooder object to move

    Returns:
        A random location in the Dooder's neighborhood
    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood
        random_cell = choice(neighborhood.coordinates)

        return random_cell


@Policies.register()
class RuleBased(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood that has energy.
    A neighborhood is all surrounding positions, including the current position

    Args:
        dooder: The Dooder object to move

    Returns:
        A random location in the Dooder's neighborhood that has energy
    """
    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood
        energy = neighborhood.fetch('Energy')

        if energy:
            energy_positions = [e.position for e in energy]
            random_cell = choice(energy_positions)

        else:
            random_cell = dooder.position

        return random_cell


@Policies.register()
class NeuralNetwork(BasePolicy):
    """
    Given a Dooder object, returns a selected location based on neural network output

    Args:
        dooder: The Dooder object to move

    Returns:
        A location based on neural network output
    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        #! Need to make based on the goal (Energy or Reproduction)
        #! Need a better way to manage multiple models for a dooder
        #! Target-based movement models
        #! Need a better way to create internal models from Dooder class directly        
        
        neighborhood = dooder.neighborhood
        
        base_goals = {'Reproduce': 'Dooder', 'Consume': 'Energy'}
        
        goal = cls.infer_goal(dooder, neighborhood)
        target = base_goals[goal]
        
        # Check if the target is inside the Dooder's neighborhood
        has_target = np.array([neighborhood.contains(target)], dtype='uint8')

        # Get model if it exists, else return an empty dict
        movement_model = dooder.internal_models.get('move', {})
            
        model = movement_model.get(target, None):
            
        if model is None:
            model = SimpleNeuralNet()
            dooder.internal_models['move'][target] = model

        # Predict where to move
        prediction = model.predict(has_target)
        predicted_location = neighborhood.coordinates[prediction]

        # Learn from the reality
        # Note: Prediction happens before learning. Learning happens after action
        correct_choices = [location[0] for location in enumerate(
            neighborhood.contains(target)) if location[1] == True]

        model.learn(correct_choices)

        return predicted_location
     
     @classmethod
     def infer_goal(cls, dooder, neighborhood):
            if dooder.hunger < 0:
                return 'Consume'
            elif neighborhood.contains('Dooder'): # maybe have a way to return any, all, none, etc
                return 'Reproduce'
            else:
                return 'Consume'
    
    
    
