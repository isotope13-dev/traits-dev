"""Generate inert matching controls. PE entrypoints return immediately."""
from pathlib import Path
import runpy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
ROOT = Path(__file__).parent
image = runpy.run_path(str(ROOT.parent / 'first-review' / 'build_pe_fixtures.py'))['image']
def pe(name, strings):
    data = bytearray(image(imports=False, overlay=False, rwx=False))
    content = b'\0'.join(s.encode() for s in strings) + b'\0'
    assert len(content) < 500
    data[0x201:0x201+len(content)] = content
    (ROOT / name).write_bytes(data)
hooks = ['GetKeyboardState', 'SetWindowsHookExA', 'CallNextHookEx',
         'GetProcAddress', 'GetClipboardData']
pe('gui-hooks.exe', hooks)
pe('recording-hooks.exe', hooks + ['keystroke Logs'])
pe('report-label-only.exe', ['keystroke Logs'])
pe('ordinary-path.exe', ['PATH=C:\\Windows;C:\\Program Files\\dotnet\\;C:\\Program Files\\Python\\;C:\\Program Files\\Java\\'])
pe('noise-path.exe', ['}~abcC:\\Program Files\\alpha\\',
                      '^>xyzC:\\Program Files\\bravo\\',
                      '<{abcC:\\Program Files (x86)\\charlie\\'])
pe('browser-name-field.exe', ['GetBrowsersEmpty', 'Mozilla Thunderbird'])
key = b'0123456789abcdef0123456789abcdef'
iv = bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(b'# Harmless demonstration of an encoded greeting.\nprint("hello")\n', 16))
carrier = ''.join(chr(0xfe00 + c) if c < 16 else chr(0xe0100 + c - 16) for c in cipher)
decoder = 'ciphertext = bytes(ord(c) - 0xFE00 if ord(c) <= 0xFE0F else ord(c) - 0xE0100 + 16 for c in carrier)\n'
header = f'from Crypto.Cipher import AES\nfrom Crypto.Util.Padding import unpad\ncarrier = "{carrier}"\n'
setup = f'key = {key!r}\niv = bytes(16)\n'
(ROOT / 'harmless-encrypted-exec.py').write_text(header + decoder + setup + 'exec(unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), 16))\n')
(ROOT / 'selector-display.py').write_text(f'carrier = "{carrier}"\n' + decoder + 'print(ciphertext.hex())\n')
