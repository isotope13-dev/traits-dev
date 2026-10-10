import pickle
import zlib
import json

class Serializer:
    def legacy(self, data):
        return pickle.loads(data)

    def current(self, data):
        return json.loads(zlib.decompress(data).decode("utf8"))
