"""Recover this sample's standard Brotli-compressed Tauri assets without execution."""
import argparse
import ctypes as c
import ctypes.util
import hashlib
import json
from pathlib import Path

ASSETS = [
    ('/tauri.svg', 0x8fd144),
    ('/vite.svg', 0x8fd657),
    ('/index.html', 0x8fd928),
    ('/assets/index-CKtnZ5zA.css', 0x8fda1e),
    ('/assets/index-D74oUpkj.js', 0x8fe30a),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sample', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = args.sample.read_bytes()
    assert hashlib.sha256(data).hexdigest() == (
        'a7eab90137b449877579d066372df0c5e699f22c06d8b5a6be18c5aa13dd335f')
    library = ctypes.util.find_library('brotlidec')
    if library is None:
        library = '/opt/homebrew/lib/libbrotlidec.dylib'
    lib = c.CDLL(library)
    lib.BrotliDecoderCreateInstance.argtypes = [c.c_void_p] * 3
    lib.BrotliDecoderCreateInstance.restype = c.c_void_p
    lib.BrotliDecoderDestroyInstance.argtypes = [c.c_void_p]
    lib.BrotliDecoderDecompressStream.argtypes = [
        c.c_void_p, c.POINTER(c.c_size_t), c.POINTER(c.c_void_p),
        c.POINTER(c.c_size_t), c.POINTER(c.c_void_p), c.POINTER(c.c_size_t)]
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, offset in ASSETS:
        assert data[offset:offset + len(name)] == name.encode()
        start = offset + len(name)
        source = c.create_string_buffer(data[start:])
        output = c.create_string_buffer(8 * 1024 * 1024)
        available_in = c.c_size_t(len(data) - start)
        next_in = c.c_void_p(c.addressof(source))
        available_out = c.c_size_t(len(output))
        next_out = c.c_void_p(c.addressof(output))
        total = c.c_size_t()
        state = lib.BrotliDecoderCreateInstance(None, None, None)
        try:
            result = lib.BrotliDecoderDecompressStream(
                state, c.byref(available_in), c.byref(next_in),
                c.byref(available_out), c.byref(next_out), c.byref(total))
        finally:
            lib.BrotliDecoderDestroyInstance(state)
        assert result == 1, (name, 'Brotli decode failed or exceeded output limit')
        decoded = output.raw[:total.value]
        (args.output / Path(name).name).write_bytes(decoded)
        manifest.append({
            'name': name, 'offset': start,
            'compressed_size': len(data) - start - available_in.value,
            'decoded_size': len(decoded),
            'sha256': hashlib.sha256(decoded).hexdigest(),
        })
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
