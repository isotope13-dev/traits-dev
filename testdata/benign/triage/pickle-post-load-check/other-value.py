import pickle


def read_settings(blob, options):
    result = pickle.loads(blob)
    if not isinstance(options, dict):
        raise ValueError('expected options dict')
    return result
