"""Extract the x86 Windows DLL metadata needed by the NSIS CPU models.

Requires pefile. Reads PE structures only; does not load or execute DLLs.
Example:
  python inspect_windows_dll_metadata.py ntdll.dll kernel32.dll mshtml.dll --output dll-metadata.json

Use files from SysWOW64 on one Windows build. The optional .data bytes come
from disk, so they do not include relocations or runtime-initialized pointers.
"""
import argparse
import hashlib
import json
from pathlib import Path

import pefile


def api_hash(name):
    value = 5381
    for byte in name:
        value = ((value * 33 + byte) ^ 1547477174) & 0xffffffff
    return value


def inspect(path, include_data):
    data = path.read_bytes()
    pe = pefile.PE(data=data, fast_load=True)
    if pe.FILE_HEADER.Machine != 0x14c or pe.OPTIONAL_HEADER.Magic != 0x10b:
        raise ValueError(f'{path}: expected an x86 PE32 DLL')
    if not pe.FILE_HEADER.Characteristics & 0x2000:
        raise ValueError(f'{path}: PE header does not mark this file as a DLL')
    pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    exports = []
    for export in getattr(getattr(pe, 'DIRECTORY_ENTRY_EXPORT', None), 'symbols', []):
        exports.append({'name': None if export.name is None else export.name.decode('ascii', errors='backslashreplace'),
                        'ordinal': export.ordinal, 'rva': hex(export.address),
                        'sample_hash': None if export.name is None else hex(api_hash(export.name)),
                        'forwarder': None if export.forwarder is None else export.forwarder.decode('ascii', errors='backslashreplace')})
        if export.name in (b'BaseThreadInitThunk', b'CreateProcessInternalW') and export.forwarder is None:
            exports[-1]['code_prefix_hex'] = pe.get_data(export.address, 64).hex()
    sections = []
    for section in pe.sections:
        name = section.Name.rstrip(b'\0').decode('ascii', errors='backslashreplace')
        row = {'name': name, 'rva': hex(section.VirtualAddress),
               'virtual_size': section.Misc_VirtualSize, 'raw_size': section.SizeOfRawData,
               'file_offset': hex(section.PointerToRawData), 'characteristics': hex(section.Characteristics)}
        if name == '.data':
            raw = section.get_data()
            row['raw_sha256'] = hashlib.sha256(raw).hexdigest()
            row['zero_fill_tail_bytes'] = max(0, section.Misc_VirtualSize - len(raw))
            if include_data:
                if len(raw) > 1024 * 1024:
                    raise ValueError(f'{path}: .data exceeds the 1 MiB export bound')
                row['raw_hex'] = raw.hex()
        sections.append(row)
    optional = pe.OPTIONAL_HEADER
    result = {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'file_bytes': len(data),
              'machine': hex(pe.FILE_HEADER.Machine), 'pe_timestamp': hex(pe.FILE_HEADER.TimeDateStamp),
              'pe_offset': hex(pe.DOS_HEADER.e_lfanew), 'preferred_image_base': hex(optional.ImageBase),
              'image_size': optional.SizeOfImage, 'header_size': optional.SizeOfHeaders,
              'section_alignment': optional.SectionAlignment,
              'entry_point_rva': hex(optional.AddressOfEntryPoint),
              'sections': sections, 'exports': exports}
    result['thread_init_thunk'] = [entry for entry in exports if entry['sample_hash'] == '0x8bfb3ee0']
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('dlls', type=Path, nargs='+')
    ap.add_argument('--include-data', action='store_true')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = {'method': 'Static PE parsing only; no DLL loading or execution.',
              'runtime_data_limit': 'On-disk .data does not reproduce relocated or runtime-initialized function pointers.',
              'dlls': [inspect(path, args.include_data) for path in args.dlls]}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
