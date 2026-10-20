import pickle


def read_settings(blob):
    result = pickle.loads(blob)
    return result


def validate(result):
    if not isinstance(result, dict):
        raise ValueError('expected a dict')
    return result
