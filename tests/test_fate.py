from sdk.dooder.fate import Fate


def test_fate():
    assert type(Fate.generate_probability()) == int
    assert type(Fate.generate_score()) == int
    assert type(Fate.generate_distribution(2)) == list
    assert len(Fate.generate_distribution(2)) == 2
    assert sum(Fate.generate_distribution(2)) == 100
    assert Fate.generate_score() in range(0, 100)
    assert Fate.generate_probability() in range(0, 100)
    
def test_ask_fate():
    assert type(Fate.ask_fate(50)) == bool