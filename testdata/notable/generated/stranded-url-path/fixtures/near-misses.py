import os


def other_expressions(directory, address):
    # A hostname/prefix, query text, different delimiter, and unrelated calls
    # do not establish a joined query-stripped basename.
    prefix = os.path.join(directory, address.split('/')[0].split('?')[0])
    query = os.path.join(directory, address.split('/')[-1].split('?')[1])
    fragment = os.path.join(directory, address.split('/')[-1].split('#')[0])
    basename = address.split('/')[-1].split('?')[0]
    joined = os.path.join(directory, 'fixed-name')
    text = "os.path.join(directory, address.split('/')[-1].split('?')[0])"
    return prefix, query, fragment, basename, joined, text
