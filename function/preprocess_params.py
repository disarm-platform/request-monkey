from function.preprocess_helpers import check_if_exists, is_type


def preprocess(params: dict):
    if check_if_exists('func_name', params): 
        # Optional, but if exists, must be string
        is_type('func_name', params, str)

