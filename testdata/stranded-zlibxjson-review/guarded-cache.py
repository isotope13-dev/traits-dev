import os

def prepare_cache(cache):
    if not os.path.exists(cache):
        os.makedirs(cache, exist_ok=True)
