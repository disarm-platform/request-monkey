from function.preprocess_helpers import required_exists, is_type


def preprocess(params: dict):
    required_exists('function_name', params)

    # Optional, but if exists, must be string
    is_type('uncertainty_type', params, str)