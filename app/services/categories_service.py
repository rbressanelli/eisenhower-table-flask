from werkzeug.exceptions import BadRequest


def check_body_request(data: dict, **kwargs) -> dict:
    
    missing_keys = [ key for key in kwargs.keys() if key not in data.keys() ]
    
    if missing_keys:
        raise BadRequest(description={'error': f'missing keys: {missing_keys}'})
    
    invalid_types = {
        key:value for (key, value) in kwargs.items() if type(data[key]) != value
    }
    
    if invalid_types:
        raise BadRequest(description={'error': 'keys values must be string'})

    return {key:value.lower() for (key, value) in data.items()}
