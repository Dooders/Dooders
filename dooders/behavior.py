from random import randrange, choices, sample

def generate_probability():
    return randrange(100)

def generate_weights():
    pass

def generate_score():
    return randrange(100)

def generate_distribution(n, total):
    dividers = sorted(sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

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
    MoveDirectionDistribution = generate_distribution(9, 100)
    AwarenessScore = generate_score()
    ActionOrderDistribution = generate_distribution(3, 100)
    ActionPrivilegeScore = generate_score()
    HappinessScore = generate_score()
    EnvironmentScore = generate_score()



t = Behavior()
print(t.ActionSuccessProbability)
print(t.BreedActionProbability)


print(fate(10))
print(fate(99))