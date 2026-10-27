import pickle


def read_settings(blob):
    result = pickle.loads(blob)
    if not isinstance(result, dict):
        raise ValueError('expected a dict')
    return result
