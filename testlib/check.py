# matchers


def response_has_status_code(response, status_code):
    actual_status_code = response.status_code
    assert status_code == actual_status_code, f'''
        Expected response status code: {status_code}
        Actual status code: {actual_status_code}
    '''


def response_does_not_have_fields(response, *fields):
    json = response.json()
    unexpected_fields = [field for field in fields if json.get(field)]
    assert not unexpected_fields, f'Response contains unexpected fields: {unexpected_fields}'


def response_has_fields(response, *fields):
    json = response.json()
    missing_fields = [field for field in fields if json.get(field) is None]
    assert not missing_fields, f'Response does not have expected fields: {missing_fields}'


def response_has_only_fields(response, *fields):
    json = response.json()
    missing_fields = [field for field in fields if json.get(field) is None]
    assert not missing_fields, f'Response does not have expected fields: {missing_fields}'
    unexpected_fields = [key for key in json.keys() if key not in fields]
    assert not unexpected_fields, f'Response has unexpected fields: {unexpected_fields}'


def response_has_field_with_value(response, field, value):
    actual_field_value = response.json().get(field)
    assert actual_field_value, f'Response does not have expected {field} field'
    assert value == actual_field_value, f'''
        Expected '{field}' field value don't equal to:
        {value}
        Actual '{field}' field value:
        {actual_field_value}
    '''


def response_has_field_contains_value(response, field, value):
    actual_field_value = response.json().get(field)
    assert actual_field_value, f'Response does not have expected {field} field'
    assert value in actual_field_value, f'''
        Expected '{field}' field value doesn't contain:
        {value}
        Actual '{field}' field value:
        {actual_field_value}
    '''
