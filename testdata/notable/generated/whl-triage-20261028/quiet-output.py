import os, sys
from contextlib import contextmanager
@contextmanager
def quiet():
    with open(os.devnull, 'w') as sink:
        old_stdout,old_stderr=sys.stdout,sys.stderr
        sys.stdout=sink
        sys.stderr=sink
        try:
            yield
        finally:
            sys.stdout,sys.stderr=old_stdout,old_stderr
