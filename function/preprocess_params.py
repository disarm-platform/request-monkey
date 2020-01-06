from function.preprocess_helpers import is_type, required_exists


def preprocess(params: dict):

    if len(params) > 1:
        raise ValueError("Provide only one of function_name, random, all")
    is_type('function_name', params, str)
    is_type('all', params, bool)
    is_type('random', params, bool)
