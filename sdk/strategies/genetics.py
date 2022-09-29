from sdk.core.strategy import Strategies
    
@Strategies.register("Genetics")
def random_genetics(value: int) -> int:
    return 'working'