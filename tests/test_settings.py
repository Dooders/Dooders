# import pytest

# from sdk.core.settings import Settings


# def test_update_components():
#     settings = {'component1': 'value1', 'component2': 'value2'}
#     expected_result = {'component1': 'value1', 'component2': 'value2'}
#     s = Settings(settings)
#     result = s.update_components(settings)
#     assert result == expected_result


# def test_update_variables():
#     settings = {'variable1': 'value1', 'variable2': 'value2'}
#     expected_result = {'model1': {'variable1': 'value1', 'variable2': 'value2'},
#                        'model2': {'variable1': 'value1', 'variable2': 'value2'}}
#     s = Settings(settings)
#     result = s.update_variables(settings)
#     assert result == expected_result


# def test_get_settings_components():
#     settings = {'component1': 'value1', 'component2': 'value2'}
#     expected_result = {'component1': 'value1', 'component2': 'value2'}
#     s = Settings(settings)
#     result = s.get('components')
#     assert result == expected_result


# def test_get_settings_variables():
#     settings = {'variable1': 'value1', 'variable2': 'value2'}
#     expected_result = {'model1': {'variable1': 'value1', 'variable2': 'value2'},
#                        'model2': {'variable1': 'value1', 'variable2': 'value2'}}
#     s = Settings(settings)
#     result = s.get('variables')
#     assert result == expected_result


# def test_get_settings_variables_for_model():
#     settings = {'variable1': 'value1', 'variable2': 'value2'}
#     expected_result = {'variable1': 'value1', 'variable2': 'value2'}
#     s = Settings(settings)
#     result = s.get('variables', 'model1')
#     assert result == expected_result
