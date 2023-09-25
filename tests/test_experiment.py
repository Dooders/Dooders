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

    # def test_save_state(self, experiment):
    #     with patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment._save_state()
    #         mock_save_object.assert_called_once_with(experiment.state, 'state')

    # def test_load_state(self, experiment):
    #     with patch('builtins.open', new_callable=unittest.mock.mock_open()) as mock_open, \
    #             patch('json.load') as mock_load:
    #         experiment._load_state()
    #         mock_open.assert_called_once_with(f'experiments/{experiment.save_folder}/state.json', 'r')
    #         mock_load.assert_called_once_with(mock_open.return_value.__enter__.return_value)

    # def test_load_object(self, experiment):
    #     with patch('builtins.open', new_callable=unittest.mock.mock_open()) as mock_open, \
    #             patch('json.load') as mock_load:
    #         experiment.load_object('filename')
    #         mock_open.assert_called_once_with(f'experiments/{experiment.save_folder}/filename.json', 'r')
    #         mock_load.assert_called_once_with(mock_open.return_value.__enter__.return_value)

    # def test_get_objects(self, experiment):
    #     with patch.object(experiment.simulation.environment, 'get_objects') as mock_get_objects:
    #         experiment.get_objects('Agent')
    #         mock_get_objects.assert_called_once_with('Agent')

    #         experiment.get_objects()
    #         mock_get_objects.assert_called_with(None)

    # def test_save_experiment_results(self, experiment):
    #     with patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.save_experiment_results()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')

    # def test_load_experiment_results(self, experiment):
    #     with patch.object(experiment, 'load_object') as mock_load_object:
    #         experiment.load_experiment_results()
    #         mock_load_object.assert_called_once_with('results')

    # def test_save_passed_dooders(self, experiment):
    #     with patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.save_passed_dooders()
    #         mock_save_object.assert_called_once_with(experiment.passed_dooders, 'passed_dooders')

    # def test_load_passed_dooders(self, experiment):
    #     with patch.object(experiment, 'load_object') as mock_load_object:
    #         experiment.load_passed_dooders()
    #         mock_load_object.assert_called_once_with('passed_dooders')

    # def test_save_logs(self, experiment):
    #     with patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.save_logs()
    #         mock_save_object.assert_called_once_with(experiment.logs, 'learning_log')

    # def test_load_logs(self, experiment):
    #     with patch.object(experiment, 'load_object') as mock_load_object:
    #         experiment.load_logs()
    #         mock_load_object.assert_called_once_with('learning_log')

    # def test_save_settings(self, experiment):
    #     with patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.save_settings()
    #         mock_save_object.assert_called_once_with(experiment.settings, 'settings')

    # def test_load_settings(self, experiment):
    #     with patch.object(experiment, 'load_object') as mock_load_object:
    #         experiment.load_settings()
    #         mock_load_object.assert_called_once_with('settings')

    # def test_save_experiment(self, experiment):
    #     with patch.object(experiment, 'save_experiment_results') as mock_save_experiment_results, \
    #             patch.object(experiment, 'save_logs') as mock_save_logs, \
    #             patch.object(experiment, 'save_settings') as mock_save_settings:
    #         experiment.save_experiment()
    #         mock_save_experiment_results.assert_called_once()
    #         mock_save_logs.assert_called_once()
    #         mock_save_settings.assert_called_once()

    # def test_load_experiment(self, experiment):
    #     with patch.object(experiment, 'load_experiment_results') as mock_load_experiment_results, \
    #             patch.object(experiment, 'load_logs') as mock_load_logs, \
    #             patch.object(experiment, 'load_settings') as mock_load_settings:
    #         experiment.load_experiment()
    #         mock_load_experiment_results.assert_called_once()
    #         mock_load_logs.assert_called_once()
    #         mock_load_settings.assert_called_once()

    # def test_run(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(load=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load_and_save(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(load=True, save=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_save(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(save=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load_and_save_and_restart(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(load=True, save=True, restart=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_save_and_restart(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(save=True, restart=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load_and_restart(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(load=True, restart=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_restart(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(restart=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load_and_save_and_restart_and_custom_logic(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(load=True, save=True, restart=True, custom_logic=Mock())
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_save_and_restart_and_custom_logic(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(save=True, restart=True, custom_logic=Mock())
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load_and_restart_and_custom_logic(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(load=True, restart=True, custom_logic=Mock())
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_restart_and_custom_logic(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment:
    #         experiment.run(restart=True, custom_logic=Mock())
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()

    # def test_run_with_load_and_save_and_restart_and_custom_logic_and_save_result(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.run(load=True, save=True, restart=True, custom_logic=Mock(), save_result=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')

    # def test_run_with_save_and_restart_and_custom_logic_and_save_result(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.run(save=True, restart=True, custom_logic=Mock(), save_result=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')

    # def test_run_with_load_and_restart_and_custom_logic_and_save_result(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.run(load=True, restart=True, custom_logic=Mock(), save_result=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')

    # def test_run_with_restart_and_custom_logic_and_save_result(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object:
    #         experiment.run(restart=True, custom_logic=Mock(), save_result=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')

    # def test_run_with_load_and_save_and_restart_and_custom_logic_and_save_result_and_save_passed_dooders(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object, \
    #             patch.object(experiment, 'save_passed_dooders') as mock_save_passed_dooders:
    #         experiment.run(load=True, save=True, restart=True, custom_logic=Mock(), save_result=True, save_passed_dooders=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')
    #         mock_save_passed_dooders.assert_called_once()

    # def test_run_with_save_and_restart_and_custom_logic_and_save_result_and_save_passed_dooders(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object, \
    #             patch.object(experiment, 'save_passed_dooders') as mock_save_passed_dooders:
    #         experiment.run(save=True, restart=True, custom_logic=Mock(), save_result=True, save_passed_dooders=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')
    #         mock_save_passed_dooders.assert_called_once()

    # def test_run_with_load_and_restart_and_custom_logic_and_save_result_and_save_passed_dooders(self, experiment):
    #     with patch.object(experiment, 'load_experiment') as mock_load_experiment, \
    #             patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object, \
    #             patch.object(experiment, 'save_passed_dooders') as mock_save_passed_dooders:
    #         experiment.run(load=True, restart=True, custom_logic=Mock(), save_result=True, save_passed_dooders=True)
    #         mock_load_experiment.assert_called_once()
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')
    #         mock_save_passed_dooders.assert_called_once()

    # def test_run_with_restart_and_custom_logic_and_save_result_and_save_passed_dooders(self, experiment):
    #     with patch.object(experiment, 'simulate') as mock_simulate, \
    #             patch.object(experiment, 'save_experiment') as mock_save_experiment, \
    #             patch.object(experiment, 'save_object') as mock_save_object, \
    #             patch.object(experiment, 'save_passed_dooders') as mock_save_passed_dooders:
    #         experiment.run(restart=True, custom_logic=Mock(), save_result=True, save_passed_dooders=True)
    #         mock_simulate.assert_called_once()
    #         mock_save_experiment.assert_called_once()
    #         mock_save_object.assert_called_once_with(experiment.experiment_results, 'results')
    #         mock_save_passed_dooders.assert_called_once()
