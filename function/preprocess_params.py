from function.preprocess_helpers import required_exists, is_type


def preprocess(params: dict):
    required_exists('func_name', params)

    # Optional, but if exists, must be string
    is_type('func_name', params, str)