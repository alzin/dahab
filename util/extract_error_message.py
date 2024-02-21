import json


def extract_error_message(error_str):
    try:
        start = error_str.find('{')
        json_str = error_str[start:]
        error_json = json.loads(json_str)
        if 'error' in error_json and 'message' in error_json['error']:
            return error_json['error']['message']
        else:
            return "An unknown error occurred"
    except (ValueError, KeyError, TypeError):
        return "Failed to parse error message"
