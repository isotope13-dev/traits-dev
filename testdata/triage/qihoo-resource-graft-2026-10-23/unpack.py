"""Reconstruct ffb6b3a40802's hidden native stages without running the payload.

Usage: python3 unpack.py SAMPLE OUTPUT_DIRECTORY
Requires pefile and unicorn. Only the arithmetic decoder is emulated; its
VirtualAlloc import is replaced with a local buffer. Execution stops before
entering that buffer. PE reconstruction changes headers/relocations for analysis;
the resulting DLLs are not original downloaded artifacts.
"""
import hashlib
from pathlib import Path
import struct
import sys
import pefile
import unicorn
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

sample = Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(sample).hexdigest() == 'ffb6b3a408025aa2f9a489e847828618fbd9a33768445a6e24354d96c3cce966'
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
pe = pefile.PE(data=sample)
u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
for address, size in [(0x400000, 0x500000), (0x10000000, 0x400000),
                      (0x20000000, 0x10000), (0x30000000, 0x400000)]:
    u.mem_map(address, size)
u.mem_write(0x400000, pe.get_memory_mapped_image())
apis = {}
for descriptor in pe.DIRECTORY_ENTRY_IMPORT:
    for entry in descriptor.imports:
        address = 0x20000000 + len(apis) * 16
        apis[address] = entry.name
        u.mem_write(entry.address, struct.pack('<I', address))
u.reg_write(UC_X86_REG_ESP, 0x103ff000)
u.mem_write(0x103ff000, struct.pack('<I', 0x2000fff0))

def code_hook(emu, address, size, data):
    if address in apis:
        assert apis[address] == b'VirtualAlloc', apis[address]
        sp = emu.reg_read(UC_X86_REG_ESP)
        ret, requested, size, allocation, protection = struct.unpack('<5I', emu.mem_read(sp, 20))
        assert (requested, size, allocation, protection) == (0, 0x18d4a9, 0x3000, 0x40)
        emu.reg_write(UC_X86_REG_EAX, 0x30000000)
        emu.reg_write(UC_X86_REG_ESP, sp + 20)
        emu.reg_write(UC_X86_REG_EIP, ret)
    elif 0x30000000 <= address < 0x30400000:
        emu.emu_stop()

u.hook_add(unicorn.UC_HOOK_CODE, code_hook)
u.emu_start(0x4148a2, 0x2000fff0, count=4000000)
assert u.reg_read(UC_X86_REG_EIP) == 0x30061ca6
stage = bytes(u.mem_read(0x30000000, 0xbe008))
(out / 'decoded-stage.bin').write_bytes(stage)
length32, length64, offset32, loader32, offset64, loader64, length = struct.unpack_from('<7I', stage)
assert (length32, length64, offset32, loader32, offset64, loader64, length) == (
    0x5e106, 0x57582, 0xac0, 0x61ca6, 0x61ef6, 0xbd4b8, 0xbe000)
key = stage[28:60]

def lznt1(blob):
    result = bytearray(); pos = 0
    while pos + 2 <= len(blob):
        header = int.from_bytes(blob[pos:pos+2], 'little'); pos += 2
        if not header: break
        end = pos + (header & 0xfff) + 1
        chunk = blob[pos:end]; pos = end
        if not header & 0x8000:
            result.extend(chunk); continue
        decoded = bytearray(); i = 0
        while i < len(chunk):
            flags = chunk[i]; i += 1
            for bit in range(8):
                if i >= len(chunk): break
                if flags & (1 << bit):
                    token = int.from_bytes(chunk[i:i+2], 'little'); i += 2
                    mask = 0xfff; shift = 12; position = len(decoded) - 1
                    while position >= 0x10:
                        mask >>= 1; shift -= 1; position >>= 1
                    count = (token & mask) + 3; distance = (token >> shift) + 1
                    for _ in range(count): decoded.append(decoded[-distance])
                else:
                    decoded.append(chunk[i]); i += 1
        result.extend(decoded)
    return result

for name, offset, size, expected_size in [('x86', offset32, length32, 528896),
                                         ('x64', offset64, length64, 514560)]:
    compressed = bytes(x ^ key[i % 32] for i, x in enumerate(stage[offset:offset+size]))
    image = lznt1(compressed)
    assert len(image) == expected_size and image[:8] == b'\x89PNG\r\n\x1a\n'
    (out / (name + '-disguised.bin')).write_bytes(image)
    nt = struct.unpack_from('<I', image, 8)[0]
    image[:2] = b'MZ'; struct.pack_into('<I', image, 0x3c, nt)
    image[nt:nt+4] = b'PE\0\0'
    payload = pefile.PE(data=image)
    seed = payload.OPTIONAL_HEADER.CheckSum; rand = seed; name_key = []
    for _ in range(256):
        rand = (rand * 0x343fd + 0x269ec3) & 0xffffffff
        name_key.append(((rand >> 16) & 0x7fff) % 10)
    seen = set()
    def decode_name(rva):
        start = payload.get_offset_from_rva(rva)
        if start not in seen:
            end = image.index(0, start)
            image[start:end] = bytes(x ^ name_key[i % 256] for i, x in enumerate(image[start:end]))
            seen.add(start)
    width, form = (4, '<I') if name == 'x86' else (8, '<Q')
    directory = payload.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress
    for index in range(20):
        oft, _, _, dll_name, _ = struct.unpack_from('<5I', image,
            payload.get_offset_from_rva(directory + index * 20))
        if not dll_name: break
        decode_name(dll_name)
        for index in range(300):
            thunk = struct.unpack(form, payload.get_data(oft + index * width, width))[0]
            if not thunk: break
            if not thunk & (1 << (width * 8 - 1)): decode_name(thunk + 2)
    for block in payload.DIRECTORY_ENTRY_BASERELOC:
        for entry in block.entries:
            if entry.type == (3 if width == 4 else 10):
                pos = payload.get_offset_from_rva(entry.rva)
                struct.pack_into(form, image, pos, struct.unpack_from(form, image, pos)[0] ^ seed)
    ep = payload.OPTIONAL_HEADER.get_field_absolute_offset('AddressOfEntryPoint')
    struct.pack_into('<I', image, ep, payload.OPTIONAL_HEADER.AddressOfEntryPoint ^ seed)
    (out / (name + '-reconstructed.dll')).write_bytes(image)
    print(name, len(image), hashlib.sha256(image).hexdigest())
