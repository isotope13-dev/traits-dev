"""Utility-module pickle/frame co-location is not a config loader.

Pickle label helpers and a frame-based compat helper live tens of lines
apart in one grab-bag module; no loader reads caller globals to unpickle.
"""
import pickle
import sys
from base64 import encodebytes as _enc, decodebytes as _dec


def encode_label(args):
    return _enc(pickle.dumps(args)).strip().decode('latin1')


def decode_label(label):
    return pickle.loads(_dec(label.encode('latin1')))

# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 
# padding comment for utility module layout 

def zip_imported(ldr=None):
    if not ldr:
        ldr = sys._getframe(1).f_globals['__loader__']
    return ldr
