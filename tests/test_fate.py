from sdk.dooder.fate import Fate
    
    
def test_ask_fate():
    assert type(Fate.ask_fate(50)) == bool