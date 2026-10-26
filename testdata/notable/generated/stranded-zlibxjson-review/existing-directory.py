import os

def prepare_cache(cache):
    if os.path.exists(cache):
        os.makedirs(cache)
