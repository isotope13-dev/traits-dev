import os

def prepare_output(cache, output):
    if not os.path.exists(cache):
        os.makedirs(output)
