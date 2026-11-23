import cloudpickle

EXAMPLE = "cloudpickle.loads(payload)"
# cloudpickle.load(stream)

def encode(value):
    return cloudpickle.dumps(value)
