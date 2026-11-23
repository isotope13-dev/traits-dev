import cloudpickle

def restore(stream, payload):
    return cloudpickle.load(stream), cloudpickle.loads(payload)
