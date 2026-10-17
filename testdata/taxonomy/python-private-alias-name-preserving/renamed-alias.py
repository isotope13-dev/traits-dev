"""Malicious control: staging primitive renamed to an unrelated name."""
from subprocess import Popen as _ffcc


def run_hidden(argv):
    return _ffcc(argv)
