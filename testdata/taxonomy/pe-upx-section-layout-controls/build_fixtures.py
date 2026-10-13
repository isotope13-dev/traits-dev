#!/usr/bin/env python3
"""Build small deterministic PE controls for the writable-entry UPX profile."""
from pathlib import Path
import random
import struct


ROOT = Path(__file__).resolve().parent
PE_OFFSET = 0x80
HEADERS_SIZE = 0x400
RAW_OFFSET = 0x600
UPX_RAW_SIZE = 0x10000


def section(name: bytes, virtual_address: int, raw_offset: int, raw_size: int,
            characteristics: int, virtual_size: int | None = None) -> bytes:
    return struct.pack(
        "<8sIIIIIIHHI",
        name.ljust(8, b"\0"),
        virtual_size if virtual_size is not None else raw_size,
        virtual_address,
        raw_size,
        raw_offset,
        0,
        0,
        0,
        0,
        characteristics,
    )


def pe_bytes(*, entry_writable: bool, wx: bool, upx_label: bool,
             high_entropy: bool, many_strings: bool) -> bytes:
    text_chars = 0x60000020  # code, readable, executable
    payload_chars = 0xC0000040  # initialized data, readable, writable
    if wx:
        payload_chars |= 0x20000000
    text = section(b".text", 0x1000, 0x400, 0x200, text_chars)
    name = b"UPX1" if upx_label else b".stub"
    payload = section(name, 0x2000, RAW_OFFSET, UPX_RAW_SIZE,
                      payload_chars, UPX_RAW_SIZE)
    entry_rva = 0x2000 if entry_writable else 0x1000

    dos = bytearray(PE_OFFSET)
    dos[:2] = b"MZ"
    struct.pack_into("<I", dos, 0x3C, PE_OFFSET)
    coff = struct.pack(
        "<HHIIIHH",
        0x8664, 2, 0, 0, 0, 0xF0, 0x0022,
    )
    optional = bytearray(0xF0)
    struct.pack_into("<H", optional, 0, 0x20B)  # PE32+
    struct.pack_into("<I", optional, 16, entry_rva)
    struct.pack_into("<I", optional, 20, 0x1000)  # BaseOfCode
    struct.pack_into("<Q", optional, 24, 0x140000000)
    struct.pack_into("<I", optional, 32, 0x1000)  # SectionAlignment
    struct.pack_into("<I", optional, 36, 0x200)  # FileAlignment
    struct.pack_into("<I", optional, 56, 0x12000)  # SizeOfImage
    struct.pack_into("<I", optional, 60, HEADERS_SIZE)
    struct.pack_into("<H", optional, 68, 3)  # Windows CUI subsystem
    struct.pack_into("<H", optional, 70, 0x8160)
    struct.pack_into("<I", optional, 108, 16)  # NumberOfRvaAndSizes

    image = bytearray(HEADERS_SIZE + UPX_RAW_SIZE)
    image[:len(dos)] = dos
    image[PE_OFFSET:PE_OFFSET + 4] = b"PE\0\0"
    coff_start = PE_OFFSET + 4
    image[coff_start:coff_start + len(coff)] = coff
    optional_start = coff_start + len(coff)
    image[optional_start:optional_start + len(optional)] = optional
    sections_start = optional_start + len(optional)
    image[sections_start:sections_start + 40] = text
    image[sections_start + 40:sections_start + 80] = payload

    if high_entropy:
        data = bytearray(random.Random(72341).randbytes(UPX_RAW_SIZE))
    else:
        data = bytearray(UPX_RAW_SIZE)
    if many_strings:
        marker_bytes = b"\0".join(
            f"CONTROL_STRING_MARKER_{n:03d}".encode() for n in range(32)
        ) + b"\0"
        data[-len(marker_bytes):] = marker_bytes
    image[RAW_OFFSET:RAW_OFFSET + UPX_RAW_SIZE] = data
    return bytes(image)


CASES = {
    "positive-high-entropy-string-rich.exe": dict(
        entry_writable=True, wx=True, upx_label=True,
        high_entropy=True, many_strings=True,
    ),
    "positive-sparse-strings-low-entropy.exe": dict(
        entry_writable=True, wx=True, upx_label=True,
        high_entropy=False, many_strings=False,
    ),
    "near-miss-entry-not-writable.exe": dict(
        entry_writable=False, wx=True, upx_label=True,
        high_entropy=True, many_strings=True,
    ),
    "near-miss-no-wx-section.exe": dict(
        entry_writable=True, wx=False, upx_label=True,
        high_entropy=True, many_strings=True,
    ),
    "near-miss-no-upx-label.exe": dict(
        entry_writable=True, wx=True, upx_label=False,
        high_entropy=True, many_strings=True,
    ),
    "near-miss-no-alternative.exe": dict(
        entry_writable=True, wx=True, upx_label=True,
        high_entropy=False, many_strings=True,
    ),
}


for filename, options in CASES.items():
    (ROOT / filename).write_bytes(pe_bytes(**options))
print(f"built {len(CASES)} deterministic PE controls in {ROOT}")
