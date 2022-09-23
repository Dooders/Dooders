from sdk.conditions.conditions import Conditions


@Conditions.register('test')
def test():
    pass


def test_register():
    assert 'test' in Conditions.registry['test_conditions']
    
    
def test_infer_purpose():
    assert Conditions.infer_purpose(Conditions, test) == 'test_conditions'
    
    
def test_get_purpose():
    assert Conditions.get_purpose(Conditions, 'test') == 'test_conditions'