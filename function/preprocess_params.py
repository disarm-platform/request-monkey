from function.preprocess_helpers import is_type, required_exists


def preprocess(params: dict):
    required_exists('function_name', params): 
    is_type('function_name', params, str)
    
    

