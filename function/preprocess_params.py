# If exists, param must be of given type
def is_type(key, params: dict, param_type):
    param = params.get(key)

    if param is None:
        return

    if not isinstance(params[key], param_type):
        raise ValueError(f'Params \'{key}\' is not of type {param_type}')

def preprocess(params: dict):

    if len(params) > 1:
        raise ValueError("Provide only one of function_name, random, all")
    is_type('function_name', params, str)
    is_type('all', params, bool)
    is_type('random', params, bool)
