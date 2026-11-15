import os


def read_document(filename):
    safe_name = os.path.basename(filename)
    path = os.path.join(os.path.expanduser("~/documents"), safe_name)
    with open(path) as handle:
        return handle.read()
