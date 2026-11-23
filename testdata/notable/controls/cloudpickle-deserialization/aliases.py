import cloudpickle as cp
from cloudpickle import loads as restore

def decode(payload):
    return cp.loads(payload), restore(payload)
