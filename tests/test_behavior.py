from sdk.dooder.behavior import Behavior, BehaviorProfile, Generators


def test_generators():
    assert type(Generators.Probability()) == int
    assert type(Generators.Score()) == int
    assert type(Generators.Distribution(2)) == list
    assert len(Generators.Distribution(2)) == 2
    assert sum(Generators.Distribution(2)) == 100
    assert Generators.Score() in range(0, 100)
    assert Generators.Probability() in range(0, 100)
    
def test_behavior_profile():
    bp = BehaviorProfile()
    assert type(bp.ActionSuccessProbability) == int
    assert type(bp.TakeActionProbability) == int
    assert type(bp.ActionSelectionWeights) == list
    assert type(bp.MakeMoveProbability) == int
    assert type(bp.MoveSuccessProbability) == int
    assert type(bp.BreedSuccessProbability) == int
    assert type(bp.BreedActionProbability) == int
    assert type(bp.MoveDirectionDistribution) == list
    assert type(bp.ActionOrderDistribution) == list
    
def test_behavior():
    b = Behavior()
    assert type(b) == Behavior
    assert type(b.behavior_profiles) == list
    assert type(b.load_genetics()) == dict
    assert type(b.generate_values(b.load_genetics())) == dict
    assert type(b.generate_behavior()) == BehaviorProfile
