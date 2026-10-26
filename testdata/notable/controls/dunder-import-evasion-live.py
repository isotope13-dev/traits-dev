"""Live dunder-import evasion: base64 and zlib are dynamically imported
and applied to an embedded blob at runtime. No template registry, so the
double-dunder hostile must still fire.
"""
import sys

_b64 = __import__('base64')
_zlib = __import__('zlib')


def run(blob):
    raw = _b64.b64decode(blob)
    code = _zlib.decompress(raw)
    sys.modules[__name__].__dict__['entry'] = code
    exec(compile(code, '<stage>', 'exec'))
