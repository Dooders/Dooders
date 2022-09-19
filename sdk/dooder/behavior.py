from sdk.strategies.strategies import Strategies, compile_strategy

GeneticStrategy = Strategies.load_strategy('sdk/dooder/genetics.yml')

class Genetics:
    
    genetic_profiles = []    

    @classmethod
    def compile_genetics(cls, dooder):
        genetics = compile_strategy(dooder, GeneticStrategy)
        cls.genetic_profiles.append(genetics)
        
        return genetics
            
