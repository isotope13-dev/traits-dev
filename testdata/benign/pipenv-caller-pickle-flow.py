import pickle, zlib, sys
caller = sys._getframe(1).f_globals
result = pickle.loads(zlib.decompress(data))
