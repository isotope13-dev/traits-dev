import pickle, gzip
result = pickle.loads(gzip.decompress(data))
