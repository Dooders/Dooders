import json
import os
import unittest.mock
from unittest.mock import Mock, patch

import pytest

from dooders.experiment import Experiment


class TestExperiment:

    @pytest.fixture
    def experiment(self):
        return Experiment(experiment_name="Test", save_state=True)

    def test_create_simulation(self, experiment):
        with patch('dooders.sdk.core.Assemble.execute') as mock_execute:
            experiment.create_simulation()
            mock_execute.assert_called_once_with(experiment.settings)

    def test_simulate(self, experiment):
        with patch.object(experiment, 'create_simulation') as mock_create_simulation, \
                patch.object(experiment, '_save_state') as mock_save_state:

            mock_simulation = Mock()
            mock_simulation.run_simulation.return_value = False
            mock_create_simulation.return_value = mock_simulation

            experiment.simulate()

            mock_create_simulation.assert_called_once()
            mock_simulation.run_simulation.assert_called_once_with(
                experiment.batch, 1)
            mock_save_state.assert_called_once()

    def test_save_object(self, experiment):
        with patch('builtins.open', new_callable=unittest.mock.mock_open()) as mock_open, \
                patch('os.path.exists') as mock_exists, \
                patch('os.makedirs') as mock_makedirs, \
                patch('json.dump') as mock_dump:

            mock_exists.return_value = False
            object_to_save = {"key": "value"}
            filename = "test_filename"

            experiment.save_object(object_to_save, filename)

            save_path = f'experiments/{experiment.save_folder}/{filename}.json'
            mock_exists.assert_called_once_with(
                f'experiments/{experiment.save_folder}/')
            mock_makedirs.assert_called_once_with(
                f'experiments/{experiment.save_folder}/')
            mock_open.assert_called_once_with(save_path, 'w')
            mock_dump.assert_called_once_with(
                object_to_save, mock_open.return_value.__enter__.return_value)  # Corrected line

    # def test_load_state(self, experiment):
    #     with patch('builtins.open', new_callable=unittest.mock.mock_open()) as mock_open, \
    #             patch('json.load') as mock_load:
    #         experiment._load_state()
    #         mock_open.assert_called_once_with(
    #             f'experiments/{experiment.save_folder}/state.json', 'r')
    #         mock_load.assert_called_once_with(
    #             mock_open.return_value.__enter__.return_value)
