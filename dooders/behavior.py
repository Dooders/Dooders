from random import randrange, choices

def generate_probability():
    return randrange(100)

def generate_weights():
    pass

def generate_score():
    return randrange(100)

def generate_distribution():
    pass

def fate(weight):
    fate_list = [True, False]
    weights = (weight, 100-weight)
    return choices(fate_list, weights=weights, k=len(fate_list))[0]

class Behavior:
    ActionSuccessProbability = generate_probability()
    TakeActionProbability = generate_probability()
    ActionSelectionWeights = generate_weights()
    MakeMoveProbability = generate_probability()
    BreedSuccessProbability = generate_probability()
    BreedActionProbability = generate_probability()
    MoveDirectionDistribution = generate_distribution()
    AwarenessScore = generate_score()
    ActionOrderDistribution = generate_distribution()
    ActionPrivilegeScore = generate_score()
    HappinessScore = generate_score()
    EnvironmentScore = generate_score()



t = Behavior()
print(t.ActionSuccessProbability)
print(t.BreedActionProbability)


print(fate(10))
print(fate(99))