""" 
Movement Policy
----------------
This policy is responsible for "deciding" where a Dooder will move during it's step

Currently there are three policies:
1. Random: The Dooder will move to a random location
2. Rule-based: The Dooder will move to a location based on a set of rules
3. Neural Network: The Dooder will move to a location based on a neural network output
"""

from random import choice
from typing import TYPE_CHECKING

import numpy as np

from sdk.base.base_policy import BasePolicy
from sdk.core.core import Core

if TYPE_CHECKING:
    from sdk.models.dooder import Dooder


@Core.register('policy')
class RandomMove(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood
    A neighborhood is all surrounding positions, including the current position
    
    Parameters
    ----------
    dooder: Dooder
        The Dooder object to move

    Returns
    -------
    random_cell: tuple
        A random location in the Dooder's neighborhood
        
    Methods
    -------
    execute(dooder: Dooder) -> tuple
        Returns a random location in the Dooder's neighborhood
    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood
        random_cell = choice(neighborhood.coordinates)

        return random_cell

@Core.register('policy')
class RuleBased(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects neighborhood that has energy.
    A neighborhood is all surrounding positions, including the current position

    Parameters
    ----------
    dooder: Dooder
        The Dooder object to move

    Returns
    -------
    random_cell: tuple
        A random location in the Dooder's neighborhood that has energy
        
    Methods
    -------
    execute(dooder: Dooder) -> tuple
        Returns a random location in the Dooder's neighborhood that has energy
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

@Core.register('policy')
class NeuralNetwork(BasePolicy):
    #! Change this name to TargetBased or GoalBased
    """ 
    Given a Dooder object, returns a selected location based on neural network output
    The neural network is trained to predict the location of the nearest target source
    This function will first determine to goal of the Dooder (Reproduce or Consume)
    Then a model is trained for each target source (Dooder or Energy)

    Parameters
    ----------
    dooder: Dooder
        The Dooder object to move

    Returns
    -------
    predicted_location: tuple
        A location based on neural network output
        
    Methods
    -------
    execute(dooder: Dooder) -> tuple
        Returns a location based on neural network output
    infer_goal(dooder, neighborhood) -> str
        Returns the goal of the Dooder
    """
    #! change neighborhood to perception

    base_goals = {'Reproduce': 'Dooder', 'Consume': 'Energy'}

    @classmethod
    def execute(cls, dooder: 'Dooder') -> tuple:
        neighborhood = dooder.neighborhood

        goal = cls.infer_goal(dooder, neighborhood)
        target = cls.base_goals[goal]

        # Check if the target is inside the Dooder's neighborhood
        target_array = np.array([neighborhood.contains(target)], dtype='uint8')

        # Get model if it exists, else return an error  
        model = dooder.internal_models.get(goal, None)

        if model is None:
            # raise error
            pass
        
        # Predict where to move
        prediction = model.predict(target_array)
        predicted_location = neighborhood.coordinates[prediction]

        # Learn from the reality
        # Note: Prediction happens before learning. 
        # Learning happens after action
        correct_choices = [location[0] for location in enumerate(
            neighborhood.contains(target)) if location[1] == True]

        model.learn(correct_choices)

        return predicted_location

    @classmethod
    def infer_goal(cls, dooder, neighborhood) -> str:
        """ 
        Function to infer the goal of the Dooder
        The goal is to reproduce or consume energy
        If the Dooder has hunger below 0, it will consume energy
        If there are any Dooders nearby, it will reproduce
        The default goal is to consume energy

        Parameters
        ----------
        dooder: Dooder
            The Dooder object to move
        neighborhood: Neighborhood
            The Dooder's neighborhood

        Returns
        -------
        goal: str
            The goal of the Dooder 'Consume' or 'Reproduce'
        """
        if dooder.hunger > 0:
            return 'Consume'
        elif any(neighborhood.contains('Dooder')):
            return 'Reproduce'
        else:
            return 'Consume'
