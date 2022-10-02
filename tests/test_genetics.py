from sdk.models.genetics import Genetics
from tests.test_util import mock_simulation

simulation = mock_simulation()
    
def test_genetics():
    bp = Genetics()
    bp.compile_genetics(simulation)
    assert len(bp.genetic_profiles) >= 1

    
