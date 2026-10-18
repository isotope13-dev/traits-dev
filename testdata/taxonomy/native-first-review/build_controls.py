"""Build inert PE controls; their sole instruction returns immediately."""
import json
import struct
import sys
from pathlib import Path

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)

def pe(data):
    image = bytearray(32768)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', image, opt, 0x10b)
    struct.pack_into('<III', image, opt+4, 512, 31744, 0)
    struct.pack_into('<III', image, opt+16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', image, opt+28, 0x400000, 0x1000, 512)
    struct.pack_into('<HH', image, opt+40, 4, 0)
    struct.pack_into('<II', image, opt+56, 0xa000, 512)
    struct.pack_into('<H', image, opt+68, 3)
    struct.pack_into('<IIIIII', image, opt+72, 0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    for i, (name, va, size, offset, flags) in enumerate([
        (b'.text', 0x1000, 512, 512, 0x60000020),
        (b'.data', 0x2000, 31744, 1024, 0xc0000040),
    ]):
        sec = opt+224+i*40
        image[sec:sec+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', image, sec+8, size, va, size, offset)
        struct.pack_into('<I', image, sec+36, flags)
    image[512] = 0xc3
    image[1024:1024+len(data)] = data
    return image

api = b'\0'.join(s.encode() for s in [
    'urlmon.dll', 'wininet.dll', 'InternetOpenA', 'InternetConnectA',
    'HttpOpenRequestA', 'HttpSendRequestA', 'InternetReadFile',
    'InternetCloseHandle', 'HttpQueryInfoA',
    'HttpSendRequestExA', 'HttpEndRequestA', 'ObtainUserAgentString',
]) + b'\0'
wallet = '48' + 'A'*93
config = {'pools': [{'algo': 'cn/r', 'url': 'stratum+tcp://pool.example:3333',
                     'user': wallet}], 'donate-level': 0}
for name, data in [
    ('http-apis.exe', api),
    ('http-missing-extended.exe', api.replace(b'HttpSendRequestExA', b'OtherRequestName__').replace(b'HttpEndRequestA', b'OtherEndName___')),
    ('mining-config.exe', b'xmrig\0' + json.dumps(config).encode() + b'\0'),
    ('mining-config-no-cn.exe', b'xmrig\0' + json.dumps(config).replace('cn/r', 'rx/0').encode() + b'\0'),
    ('mining-config-donate.exe', b'xmrig\0' + json.dumps(config).replace('"donate-level": 0', '"donate-level": 1').encode() + b'\0'),
]:
    (out/name).write_bytes(pe(data))
