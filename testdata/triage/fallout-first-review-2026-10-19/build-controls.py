"""Build inert section fixtures and semantic near misses from reviewed code."""
import json
import struct
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
sample = Path(sys.argv[1]).read_bytes()
cases = []
xor_id = 'micro-behaviors/data/codec::arm-four-byte-cyclic-xor-buffer-loop'
rc4_id = 'micro-behaviors/crypto/symmetric/stream/rc4::arm-rc4-eight-byte-key-buffer-transform'


def emit(name, code, expected=(), machine=40, section='.text'):
    # No program headers and no entry point: these are section fixtures.
    names = b'\0' + section.encode() + b'\0.shstrtab\0'
    data = bytearray(0x700)
    data[:52] = struct.pack('<16sHHIIIIIHHHHHH',
        b'\x7fELF\x01\x01\x01' + b'\0' * 9,
        2, machine, 1, 0, 0, 0x600, 0, 52, 0, 0, 40, 3, 2)
    data[0x100:0x100 + len(code)] = code
    data[0x580:0x580 + len(names)] = names
    struct.pack_into('<10I', data, 0x628,
                     1, 1, 6 if section == '.text' else 2,
                     0x10100, 0x100, len(code), 0, 0, 4, 0)
    struct.pack_into('<10I', data, 0x650,
                     len(section) + 2, 3, 0, 0, 0x580, len(names), 0, 0, 1, 0)
    path = root / name
    path.write_bytes(data)
    cases.append({'path': str(path.relative_to(root.parents[2])),
                  'matched': list(expected),
                  'not_matched': [x for x in (xor_id, rc4_id) if x not in expected]})


tx = sample[0xc0f4:0xc128]
rx = sample[0xbff0:0xc028]
rc4 = sample[0xa7a0:0xa86c]
emit('xor-transmit.elf', tx, [xor_id])
emit('xor-receive.elf', rx, [xor_id])
emit('xor-arithmetic.elf', tx.replace(bytes.fromhex('01 20 22 E0'),
                                    bytes.fromhex('01 20 82 E0')))
emit('xor-eight-byte-cycle.elf', tx.replace(bytes.fromhex('03 30 03 E2'),
                                          bytes.fromhex('07 30 03 E2')))
emit('xor-without-loop.elf', tx[:-4] + bytes.fromhex('00 00 A0 E1'))
emit('xor-rodata.elf', tx, section='.rodata')
emit('xor-wrong-architecture.elf', tx, machine=3)
emit('rc4-transform.elf', rc4, [rc4_id])
emit('rc4-without-state-swap.elf',
     rc4.replace(bytes.fromhex('04 20 CC E7'), bytes.fromhex('00 00 A0 E1')))
emit('rc4-without-output-xor.elf',
     rc4.replace(bytes.fromhex('05 30 23 E0'), bytes.fromhex('05 30 83 E0')))
emit('rc4-rodata.elf', rc4, section='.rodata')
emit('rc4-wrong-architecture.elf', rc4, machine=3)
(root / 'cases.json').write_text(json.dumps({'id_map': {}, 'fixtures': cases}, indent=2) + '\n')
