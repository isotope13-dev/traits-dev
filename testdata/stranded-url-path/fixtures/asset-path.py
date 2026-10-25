import os


def cached_asset(directory, address):
    return os.path.join(directory, address.split('/')[-1].split('?')[0])
