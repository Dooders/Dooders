import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from dooders.sdk.simulation import Simulation


class TestSimulation(unittest.TestCase):

    def setUp(self):
        settings = {'MaxCycles': 10}
        self.simulation = Simulation(settings)

    def test_setup(self):
        self.simulation.resources = Mock()
        self.simulation.arena = Mock()
        self.simulation.setup()

        self.assertTrue(self.simulation.running)
        self.simulation.resources.allocate_resources.assert_called_once()
        self.simulation.arena.generate_seed_population.assert_called_once()

    def test_step(self):
        self.simulation.time = Mock()
        self.simulation.resources = Mock()
        self.simulation.arena = Mock()
        with patch.object(Simulation, 'step') as mock_step:
            self.simulation.step()
            mock_step.assert_called_once()

    def test_cycle(self):
        with patch.object(Simulation, 'stop_conditions') as mock_stop_conditions, \
                patch.object(Simulation, 'step') as mock_step:
            mock_stop_conditions.return_value = True
            self.simulation.cycle()
            mock_step.assert_called_once()

    def test_run_simulation(self):
        max_cycles = 10
        settings = {'MaxCycles': max_cycles}
        self.simulation = Simulation(settings)

        with patch.object(Simulation, 'stop_conditions') as mock_stop_conditions, \
                patch.object(Simulation, 'step') as mock_step:
            mock_stop_conditions.side_effect = [
                True] * (max_cycles - 1) + [False]

            self.simulation.run_simulation()

            self.assertEqual(mock_step.call_count, max_cycles - 1)

    def test_reset(self):
        with patch.object(Simulation, '__init__') as mock_init, \
                patch.object(Simulation, 'setup') as mock_setup:
            mock_init.return_value = None  # as it is called in reset
            self.simulation.reset()
            mock_init.assert_called_once_with(self.simulation.settings)
            mock_setup.assert_called_once()

    def test_stop(self):
        self.simulation.stop()
        self.assertFalse(self.simulation.running)

    def test_simulation_summary(self):
        self.simulation.starting_time = datetime.now()
        self.simulation.ending_time = datetime.now()
        summary = self.simulation.simulation_summary
        self.assertIn('ElapsedSeconds', summary)

    def test_simulation_summary(self):
        self.simulation.starting_time = datetime.now()
        self.simulation.ending_time = datetime.now()

        # Mock Information.data
        mock_data = {
            'resources': {
                'allocated_energy': [10, 20],
                'consumed_energy': [5, 15]
            }
        }

        # Mock self.arena.active_dooders to have some length
        self.simulation.arena = Mock(active_dooders=[1, 2, 3])

        with patch.dict('dooders.sdk.models.information.Information.data', mock_data):
            summary = self.simulation.simulation_summary

        self.assertIn('ElapsedSeconds', summary)
        self.assertIn('TotalEnergy', summary)
        self.assertEqual(summary['TotalEnergy'], 30)  # 10 + 20
        self.assertIn('ConsumedEnergy', summary)
        self.assertEqual(summary['ConsumedEnergy'], 20)  # 5 + 15
        
    def test_generate_id(self):
        id = self.simulation.generate_id()
        self.assertIsInstance(id, str)
    
    def test_random_dooder(self):
        self.simulation.arena = Mock(active_dooders=[1, 2, 3])
        dooder = self.simulation.random_dooder()
        self.assertIsInstance(dooder, Mock)

    def test_state(self):
        self.simulation.arena = Mock()
        self.simulation.environment = Mock()
        self.simulation.time = Mock()
        self.simulation.time.time = 10
        self.simulation.starting_time = datetime.now()
        self.simulation.ending_time = datetime.now()
        self.simulation.information = Mock()
        state = self.simulation.state
        self.assertIn('simulation_id', state)
        self.assertIn('running', state)
        self.assertIn('starting_time', state)
        self.assertIn('ending_time', state)
        self.assertIn('arena', state)
        self.assertIn('environment', state)
        self.assertIn('information', state)
        