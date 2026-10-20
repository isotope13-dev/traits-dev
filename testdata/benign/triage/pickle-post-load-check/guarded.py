import pickle


def read_settings(blob):
    try:
        settings = pickle.loads(blob)
    except Exception as exc:
        raise ValueError('bad settings') from exc
    if not isinstance(settings, dict):
        raise ValueError('expected a dict')
    return settings
