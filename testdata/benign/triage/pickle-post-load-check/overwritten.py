import pickle


def read_settings(blob):
    try:
        result = pickle.loads(blob)
        result = {}
    except Exception:
        raise ValueError('bad settings')
    if not isinstance(result, dict):
        raise ValueError('expected a dict')
    return result


def finalizer(blob):
    try:
        result = pickle.loads(blob)
    finally:
        result = {}
    if not isinstance(result, dict):
        raise ValueError('expected a dict')
    return result
