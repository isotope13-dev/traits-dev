"""Generate inert CLR constructor/provenance controls; never execute them."""
import importlib.util
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('constructors', ROOT / 'testdata/first-reasoned-native-managed/check.py')
constructors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(constructors)


def control(module, downloads):
    body = constructors.managed(module=module, attribute=False)
    path = (r'C:\Users\builder\Downloads\library-master\bin\library.pdb' if downloads
            else r'C:\build\library\bin\library.pdb').encode() + b'\0'
    cv = b'RSDS' + bytes(16) + struct.pack('<I', 1) + path
    # One IMAGE_DEBUG_DIRECTORY and its CodeView record inside .text.
    struct.pack_into('<II', body, 0x98 + 96 + 6 * 8, 0x1d00, 28)
    struct.pack_into('<IIHHIIII', body, 0xf00, 0, 0, 0, 0, 2, len(cv), 0x1d20, 0xf20)
    body[0xf20:0xf20 + len(cv)] = cv
    if module and downloads:
        label = b"Clipboard copied content\0"
        body[0x1000:0x1000 + len(label)] = label
    return body


if __name__ == '__main__':
    dest = ROOT / 'testdata/benign/managed-module-provenance'
    dest.mkdir(parents=True, exist_ok=True)
    for name, module, downloads in [
        ('constructor-downloads.dll', True, True),
        ('constructor-build.dll', True, False),
        ('class-constructor-downloads.dll', False, True),
    ]:
        (dest / name).write_bytes(control(module, downloads))
