from sdk.core.strategy import Strategies


def test_register():
    @Strategies.register('Generation')
    class TestStrategy:
        pass

    assert 'TestStrategy' in Strategies.strategies['Generation']
    assert Strategies.strategies['Generation']['TestStrategy'] == TestStrategy
    
    
def test_get():
    @Strategies.register('Generation')
    class TestStrategy:
        pass

    assert Strategies.get('TestStrategy', 'Generation') == TestStrategy
