import pickle, zlib
blob = zlib.decompress(data)
result = pickle.loads(blob)
