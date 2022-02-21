from werkzeug.exceptions import BadRequest


def check_data(data: list):
    
    data_checked = [category for category in data if type(category) == str]
    
    if not data_checked:
        raise BadRequest(description={'error': 'Categories names must be string type'})
    
    return [value.lower() for value in data_checked]
