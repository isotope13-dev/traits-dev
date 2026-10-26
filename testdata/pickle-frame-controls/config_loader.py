"""Tight pickle config loader: caller-frame inspection beside unpickling."""
import pickle
import sys


def _load_config(path):
    g = sys._getframe(1).f_globals
    data = open(path, "rb").read()
    cfg = pickle.loads(data)
    blob = pickle.dumps(cfg)
    if not isinstance(cfg, dict):
        raise TypeError("bad config")
    return cfg
