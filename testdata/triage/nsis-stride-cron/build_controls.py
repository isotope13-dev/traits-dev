"""Deterministic controls for register binding, stride variation and cron grammar."""
from pathlib import Path
import zipfile
root = Path(__file__).parent
# Native API command syntax is public NSIS System syntax; no specimen names,
# sizes, keys or exact stride are necessary for the positive.
command = ('kernel32::CreateFileA(m r4 , i 0x80000000, i 0, p 0, i 4, i 0x80, i 0)i.r5H'
           'kernel32::VirtualAlloc(i 0,i 8192, i 0x3000, i 0x40)p.r7H'
           'kernel32::ReadFile(i r5, i r7, i 8192,*i 0, i 0)i.r3H'
           'user32::EnumWindows(i r7 ,i 0)')
def archive(name, text, stride, prefix=1):
    data = bytearray(b'\0' * (prefix + len(text)*stride))
    data[prefix::stride] = text.encode()
    with zipfile.ZipFile(root / name, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('commands.dat', data)
archive('bound-commands.zip', command, 17)
archive('other-stride-register.zip', command.replace('r7','r2').replace('8192','65536'), 83, 19)
archive('callback-register-mismatch.zip', command.replace('EnumWindows(i r7','EnumWindows(i r8'), 17)
archive('read-register-mismatch.zip', command.replace('ReadFile(i r5, i r7','ReadFile(i r5, i r8'), 17)
archive('read-only-allocation.zip', command.replace('i 0x40)p.r7','i 0x04)p.r7'), 17)
archive('plain-commands.zip', command, 1)
(root/'jsdoc.js').write_text('const documentation = "* @param root The root DOM element\\n* @return The iterator";\n')
macros = ['reboot','hourly','daily','weekly','monthly','yearly','annually','midnight']
for macro in macros:
    (root/f'cron-{macro}.js').write_text(f'const entry = "@{macro} root /usr/bin/true\\n";\n')
(root/'cron-numeric.js').write_text('const entry = "*/5 * * * * root /usr/bin/true\\n";\n')
# Valid SIMD instructions followed by genuine jump targets. Junk bytes are
# unreachable; the negative keeps SIMD but falls through instead of jumping.
block = bytes.fromhex('66 0f d8 cc eb 14') + bytes(range(20))
for name, data in [('simd-jumps.zip', block*3), ('simd-fallthrough.zip', (bytes.fromhex('66 0f d8 cc 90 90')+bytes(range(20)))*3)]:
    with zipfile.ZipFile(root/name, 'w', zipfile.ZIP_DEFLATED) as z: z.writestr('native.dat',data)

# Data-only WebClient observation versus source-map and filesystem near misses.
for name, data in {
    'openread-network.zip': b'\x00WebClient.Op`e`nRead\x00',
    'openread-sourcemap.zip': b'\x00"handleToggleOpen","unreadCount"\x00',
    'openread-filesystem.zip': b'\x00File.OpenRead\x00',
}.items():
    with zipfile.ZipFile(root/name, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('resource.dat', data)
