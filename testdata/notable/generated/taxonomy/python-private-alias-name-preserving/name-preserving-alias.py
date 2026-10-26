"""Benign control: name-preserving private alias.

`_SubprocessPopen` keeps the original name intact, so `grep -n Popen`
still finds it. It hides nothing, unlike a rename to an unrelated name.
"""
from subprocess import PIPE as _SUBPROCESS_PIPE
from subprocess import Popen as _SubprocessPopen


def run_helper(argv):
    result = _SubprocessPopen(argv, stdout=_SUBPROCESS_PIPE, text=True)
    return result.communicate()[0]
