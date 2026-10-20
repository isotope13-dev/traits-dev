import json


def read_settings(blob):
    result = json.loads(blob)
    if not isinstance(result, dict):
        raise ValueError('expected a dict')
    return result
