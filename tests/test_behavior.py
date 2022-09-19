from sdk.dooder.behavior import Behavior
from tests.test_util import mock_simulation

simulation = mock_simulation()
    
def test_behavior():
    bp = Behavior()
    bp.compile_behavior(simulation)
    assert len(bp.behavior_profiles) >= 1

    
