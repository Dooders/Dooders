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

from dooders.sdk.base.base_policy import BasePolicy
from dooders.sdk.core.core import Core

if TYPE_CHECKING:
    from dooders.sdk.models.dooder import Dooder


@Core.register('policy')
class RandomMove(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects perception
    A perception is all surrounding positions, including the current position

    Parameters
    ----------
    dooder: Dooder
        The Dooder object to move

    Returns
    -------
    random_cell: tuple
        A random location in the Dooder's perception

    Methods
    -------
    execute(dooder: Dooder) -> tuple
        Returns a random location in the Dooder's perception
    """

    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        perception = dooder.perception
        random_cell = choice(perception.coordinates)

        return random_cell


@Core.register('policy')
class RuleBased(BasePolicy):
    """
    Given a Dooder object, returns a random location in the objects perception that has energy.
    A perception is all surrounding positions, including the current position

    Parameters
    ----------
    dooder: Dooder
        The Dooder object to move

    Returns
    -------
    random_cell: tuple
        A random location in the Dooder's perception that has energy

    Methods
    -------
    execute(dooder: Dooder) -> tuple
        Returns a random location in the Dooder's perception that has energy
    """
    @classmethod
    def execute(self, dooder: 'Dooder') -> tuple:
        perception = dooder.perception
        energy = perception.fetch('Energy')

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
    infer_goal(dooder, perception) -> str
        Returns the goal of the Dooder
    """

    base_goals = {'Reproduce': 'Dooder', 'Consume': 'Energy'}

    @classmethod
    def execute(cls, dooder: 'Dooder') -> tuple:
        perception_spaces = dooder.perception

        inferred_goal = cls.infer_goal(dooder, perception_spaces)
        primary_target = cls.base_goals[inferred_goal]

        # Check if the target is inside the Dooder's perception
        # target_array = np.array(
        #     [perception_spaces.contains(primary_target)], dtype='uint8')
        target_array = perception_spaces.array(
            ['Energy', 'Dooder'])  # ! Temporary

        # Get model if it exists, else return an error
        model = dooder.internal_models.get(inferred_goal, None)

        if model is None:
            # raise error
            pass

        # Predict where to move
        prediction = model.predict(target_array)
        predicted_location = perception_spaces.coordinates[prediction]

        # Learn from the reality
        # Note: Inference (prediction) happens before learning.
        # Learning happens after action is taken
        correct_choices = [location[0] for location in enumerate(
            perception_spaces.contains(primary_target)) if location[1] == True]

        model.learn(correct_choices)

        inference_record = {'action': 'movement',
                            'hunger': dooder.hunger,
                            'position': dooder.position,
                            'perception': [str(x) for x in target_array[0]],
                            'decision': str(prediction),
                            'reality': [str(choice) for choice in correct_choices],
                            'inferred_goal': str(inferred_goal),
                            'accurate': prediction in correct_choices if correct_choices else None}

        dooder.inference_record[dooder.simulation.cycle_number] = inference_record

        return predicted_location

    @classmethod
    def infer_goal(cls, dooder, perception) -> str:
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
        perception: Perception
            The Dooder's perception

        Returns
        -------
        goal: str
            The goal of the Dooder 'Consume' or 'Reproduce'
        """
        if dooder.hunger > 0:
            return 'energy_detection'
        elif any(perception.contains('Dooder')) and dooder.age >= 5:
            return 'dooder_detection'
        else:
            return 'energy_detection'
