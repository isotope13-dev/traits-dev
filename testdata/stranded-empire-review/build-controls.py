"""Build inert PE string controls for clipboard trace-evidence combinations."""
import struct
from pathlib import Path

root = Path(__file__).parent

def pe(labels):
    # One non-writable .text section. Entry point is RET; remaining bytes are
    # unreachable strings, never a runnable collection implementation.
    data = bytearray(1536)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x22)
    o = 0x98
    struct.pack_into('<H', data, o, 0x20b)
    struct.pack_into('<I', data, o + 4, 1024)
    struct.pack_into('<II', data, o + 16, 0x1000, 0x1000)
    struct.pack_into('<Q', data, o + 24, 0x140000000)
    struct.pack_into('<II', data, o + 32, 0x1000, 0x200)
    struct.pack_into('<II', data, o + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, o + 68, 3)
    struct.pack_into('<I', data, o + 108, 16)
    s = o + 240
    data[s:s+8] = b'.text\0\0\0'
    struct.pack_into('<IIII', data, s + 8, 1024, 0x1000, 1024, 0x200)
    struct.pack_into('<I', data, s + 36, 0x60000020)
    body = b'\xc3\x00' + b'\x00'.join(x.encode() for x in labels) + b'\x00'
    body += b'Clipboard Copied: \0'
    data[0x200:0x200+len(body)] = body
    return data

labels = ['AddClipboardFormatListener', 'TextWriterTraceListener']
for name, words in [('trace-evidence.exe', labels),
                    ('no-listener.exe', labels[1:]),
                    ('no-file-trace.exe', labels[:1])]:
    (root / name).write_bytes(pe(words))
(root / 'no-copy-label.exe').write_bytes(pe(labels).replace(
    b'Clipboard Copied: ', b'X' * len(b'Clipboard Copied: ')))
