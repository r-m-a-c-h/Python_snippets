def external_api():
    return 10

def function_to_test(api_function):
    return api_function() + 5

def test_mocking(mocker):
    mock = mocker.patch('__main__.external_api', return_value=20)
    result = function_to_test(external_api)
    assert result == 25
    