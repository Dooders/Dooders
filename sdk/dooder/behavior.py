from sdk.strategies.strategies import Strategies, compile_strategy

BehaviorStrategy = Strategies.load_strategy('sdk/dooder/genetics.yml')

class Behavior:
    
    behavior_profiles = []    

    @classmethod
    def compile_behavior(cls, dooder):
        behavior = compile_strategy(dooder, BehaviorStrategy)
        cls.behavior_profiles.append(behavior)
        
        return behavior
            