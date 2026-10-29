#!/usr/bin/env python3
"""Check PE code bindings and neutral licensing cues without executing samples."""
import argparse
import json
import lzma
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = str(Path(os.environ.get('CLEAVE', ROOT.parent / 'cleave/target/release/cleave')).resolve())
TRAITS = Path(os.environ.get('CLEAVE_TRAITS_DIR', ROOT)).resolve()
HOOK = 'micro-behaviors/process/inject/runtime/inline-hook::x86-kernel-object-reference-detour-body'
HOOK_INTENT = 'objectives/evasion/process/hook/inline::kernel-object-reference-prologue-detour'
SOCKET = 'micro-behaviors/communications/socket/interface::native-socket-recreate-close-callback'
SAMPLES = ROOT / 'testdata/hostile/samples/pe-vt-review-20261029'
EARLIER_SAMPLES = ROOT / 'testdata/hostile/samples/pe-bad-20261028'
CAPTURE_PATCH = 'micro-behaviors/process/inject/runtime/inline-hook::x86-scanned-callsite-string-capture-patch'
CAPTURE_INTENT = 'objectives/collection/app-data/hook::scanned-code-string-capture-upload-client'
PIVOT = 'micro-behaviors/process/inject/runtime/thread-context::x86-pe-section-write-entry-context-pivot'
HOLLOWING = 'objectives/evasion/process/injection/hollowing/runtime::concealed-native-section-context-hollowing'


def signature(hex_string):
    return re.escape(bytes.fromhex(hex_string))


def unique(pattern, data):
    matches = list(re.finditer(pattern, data, flags=re.DOTALL))
    assert len(matches) == 1, (pattern.hex(), len(matches))
    return matches[0].start()


def licensing_pe(payload, pdb=False, pdb_name='adobe_licensing_wf_acro'):
    """A PE32 with one RET, read-only data, and an optional CodeView record."""
    data = bytearray(2560)
    data[:16] = bytes.fromhex('4D 5A 90 00 03 00 00 00 04 00 00 00 FF FF 00 00')
    struct.pack_into('<I', data, 60, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HH', data, 0x84, 0x14c, 2)
    struct.pack_into('<HH', data, 0x94, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<III', data, opt+16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', data, opt+28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', data, opt+56, 0x3000, 0x200)
    struct.pack_into('<H', data, opt+68, 3)
    struct.pack_into('<I', data, opt+92, 16)
    for i, (name, rva, offset, size, flags) in enumerate((
            (b'.text', 0x1000, 512, 1024, 0x60000020),
            (b'.rdata', 0x2000, 1536, 1024, 0x40000040))):
        sec = opt + 224 + i*40
        data[sec:sec+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', data, sec+8, size, rva, size, offset)
        struct.pack_into('<I', data, sec+36, flags)
    data[512] = 0xc3
    if pdb:
        cv = b'RSDS' + bytes(16) + struct.pack('<I', 1) + b'C:\\build\\' + pdb_name.encode() + b'.pdb\0'
        struct.pack_into('<II', data, opt+96+6*8, 0x2000, 28)
        struct.pack_into('<IIHHIIII', data, 1536, 0, 1, 0, 0, 2, len(cv), 0x2020, 1568)
        data[1568:1568+len(cv)] = cv
    assert len(payload) < 768
    data[1664:1664+len(payload)] = payload
    return data


def cases():
    for prefix in ('5be4e7fc1a85', '7bf7988a37a4'):
        original = lzma.decompress((SAMPLES / (prefix+'.sys.xz')).read_bytes())
        template = unique(signature('C6 45') + b'.' + signature('8B C6 45') + b'.' +
                          signature('55 C6 45') + b'.' + signature('8B C6 45') + b'.' +
                          signature('EC C6 45') + b'.' + signature('E9'), original)
        target = unique(signature('8B 1D') + b'.{4}' + signature('6A 00 8D 45') + b'.' +
                        signature('50 FF 75 14 8D 75'), original)
        reinstall = unique(signature('8B FB 8D 75') + b'.' + b'\xb8.{4}\x75.' +
                           signature('2B C3 83 E8 05 89 45') + b'.' + signature('A5 A4'), original)
        yield prefix+'-original', original, {HOOK: True}, False
        moved = bytearray(original)
        saved = moved[template:template+20]
        moved[template:template+20] = bytes(20)
        moved += bytes(16384) + saved
        yield prefix+'-unrelated-overlay-template', moved, {HOOK: False, HOOK_INTENT: False}, False
        wrong = bytearray(original)
        wrong[target+17] ^= 0x10
        yield prefix+'-wrong-restore-source', wrong, {HOOK: False, HOOK_INTENT: False}, False
        wrong = bytearray(original)
        wrong[reinstall+4] ^= 0x20
        yield prefix+'-wrong-reinstall-source', wrong, {HOOK: False, HOOK_INTENT: False}, False
        wrong = bytearray(original)
        wrong[reinstall+19] ^= 0x20
        yield prefix+'-wrong-jump-operand', wrong, {HOOK: False, HOOK_INTENT: False}, False

    original = lzma.decompress((SAMPLES / '1dee7a85bda0.exe.xz').read_bytes())
    copy = unique(signature('8B 43 4C 8B 4D') + b'.' + signature('C7 45 FC FF FF FF FF 89 41 4C'), original)
    connect = unique(signature('8B 43 44 8D 4B 10 50 51 8B 4D') + b'.\xe8', original)
    yield 'socket-original', original, {SOCKET: True}, False
    decoy = bytearray(original)
    decoy[0x40:0x40+45] = original[copy:copy+45]
    yield 'socket-earlier-noncode-copy', decoy, {SOCKET: True}, False
    wrong = bytearray(original)
    # Retarget the real call into its own following instruction, preserving
    # all imports, code fragments, UI controls and capacity counters.
    struct.pack_into('<i', wrong, connect+12, 0)
    yield 'socket-call-does-not-reach-connect', wrong, {SOCKET: False}, False

    debug = 'metadata/binary/debug::adobe-licensing-workflow-pdb'
    helper = 'metadata/binary/debug::adobe-licensing-helper-pdb-text'
    yield 'ordinary-workflow-codeview', licensing_pe(b'ordinary licensing utility\0', True), {debug: True}, True
    for module in ('kinit', 'java', 'groove', 'protocolhandler'):
        yield 'ordinary-'+module+'-codeview', licensing_pe(b'ordinary module\0', True, module), {
            'metadata/binary/debug::'+module+'-pdb': True,
            'objectives/evasion/masquerade/debug::'+module+'-pdb': False,
        }, True
    payload = b'\0'.join((b'adobe_licensing_wf_helper_acro.pdb', b'https://acrobatoauth.adobe.com/',
                          b'adobe_licensing_wf.exe', b'adobe_licensing_wf_acro.exe',
                          b'adobe_licensing_wf_helper_acro.exe', b'JQ525L2MZD.com.adobe.NGL',
                          b'x-user-token', b'access_token', b'device_token', b'new_device_token')) + b'\0'
    ordinary = licensing_pe(payload, True)
    ordinary += bytes(600000-len(ordinary))
    yield 'ordinary-licensing-context', ordinary, {debug: True, helper: True}, True
    embedded = ordinary + licensing_pe(b'first inert child\0') + licensing_pe(b'second inert child\0')
    yield 'ordinary-licensing-with-embedded-pe', embedded, {debug: True, helper: True,
        'metadata/binary/layout/embedded::unsigned-multipe-adobe-helper-debug-text': True}, True

    original = lzma.decompress(next(EARLIER_SAMPLES.glob('504dc*.xz')).read_bytes())
    install = unique(signature('C6 44 24 04 E8 C6 44 24 09 90 C6 44 24 0A 90 B8'), original) + 15
    protect = unique(signature('8D 45') + b'.' + signature('50 6A 04 56 8B 5D') + b'.' +
                     b'\x53\xa1.{4}' + signature('8B 00 50 E8'), original)
    copy_write = unique(signature('8B CE 8B 55') + b'.' + signature('8B 45') + b'.\xe8', original)
    yield 'capture-original', original, {CAPTURE_PATCH: True, CAPTURE_INTENT: True}, False
    wrong = bytearray(original)
    wrong[install+1] ^= 0x10
    yield 'capture-wrong-installed-handler', wrong, {CAPTURE_PATCH: False, CAPTURE_INTENT: False}, False
    wrong = bytearray(original)
    wrong[install+7] ^= 0x10
    yield 'capture-wrong-scan-result', wrong, {CAPTURE_PATCH: False, CAPTURE_INTENT: False}, False
    wrong = bytearray(original)
    struct.pack_into('<i', wrong, install+48, 0)
    yield 'capture-wrong-patch-writer', wrong, {CAPTURE_PATCH: False, CAPTURE_INTENT: False}, False
    wrong = bytearray(original)
    struct.pack_into('<i', wrong, protect+20, 0)
    yield 'capture-wrong-protection-call', wrong, {CAPTURE_PATCH: False, CAPTURE_INTENT: False}, False
    wrong = bytearray(original)
    wrong[copy_write+7] ^= 4
    yield 'capture-wrong-write-destination', wrong, {CAPTURE_PATCH: False, CAPTURE_INTENT: False}, False
    wrong = bytearray(original)
    struct.pack_into('<i', wrong, copy_write+9, 0)
    yield 'capture-wrong-copy-function', wrong, {CAPTURE_PATCH: False, CAPTURE_INTENT: False}, False

    original = lzma.decompress((EARLIER_SAMPLES / '683a09da2199.dll.xz').read_bytes())
    pivot = unique(signature('8B 4B 28 03 0D') + b'.{4}\x68.{4}' + signature('03 0D') +
                   b'.{4}' + signature('89 8D'), original)
    section = unique(signature('8B 47 0C 03 05') + b'.{4}' + signature('8D 55') + b'.' +
                     signature('52 89 45') + b'.' + signature('8B 57 10'), original)
    yield 'hollowing-original', original, {PIVOT: True, HOLLOWING: True}, False
    wrong = bytearray(original)
    wrong[pivot+22] ^= 4
    yield 'hollowing-wrong-entry-register', wrong, {PIVOT: False, HOLLOWING: False}, False
    wrong = bytearray(original)
    wrong[pivot+40] ^= 4
    yield 'hollowing-wrong-context-frame', wrong, {PIVOT: False, HOLLOWING: False}, False
    wrong = bytearray(original)
    wrong[section+28] ^= 4
    yield 'hollowing-wrong-process-handle', wrong, {PIVOT: False, HOLLOWING: False}, False

    # Its entire mapped image is the ncurses clear utility. Appended brands
    # belong to other PE files and must not become this carrier's VERSIONINFO.
    original = lzma.decompress((ROOT / 'testdata/suspicious/generated/pe-improve-20261029/clear-with-unexplained-overlay-prefix.exe.xz').read_bytes())
    yield 'clear-utility-with-unexplained-overlay', original, {
        'objectives/evasion/masquerade/version-resource/contradiction::packed-firewall-company-contradiction': False,
        'objectives/evasion/masquerade/identity/product::contradictory-security-product-packed-bundle': False,
    }, False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', action='append', default=[], help='Run only this named case (repeatable)')
    selected = set(parser.parse_args().case)
    fixtures = list(cases())
    unknown = selected - {name for name, *_ in fixtures}
    if unknown:
        parser.error('Unknown cases: ' + ', '.join(sorted(unknown)))
    with tempfile.TemporaryDirectory(prefix='pe-mechanism-bindings-') as temp:
        env = os.environ.copy()
        env.update(XDG_CACHE_HOME=str(Path(temp) / 'cache'), RAYON_NUM_THREADS='2')
        for name, content, expected, neutral in fixtures:
            if selected and name not in selected:
                continue
            path = Path(temp) / (name+'.exe')
            path.write_bytes(content)
            run = subprocess.run([CLEAVE, '--traits-dir', str(TRAITS), '--format', 'json', str(path)],
                                 cwd=ROOT, capture_output=True, text=True, timeout=180, env=env)
            if run.returncode != 0:
                raise SystemExit(f'{name}: scan failed\n{run.stderr[-3000:]}')
            report = json.loads(run.stdout)
            traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
            for rule, present in expected.items():
                if (rule in traits) != present:
                    raise SystemExit(f'{name}: expected {rule} present={present}; got {traits.get(rule)}')
            if neutral:
                elevated = {rule: crit for rule, crit in traits.items() if crit >= 4}
                if elevated:
                    raise SystemExit(f'{name}: neutral licensing cues raised suspicion: {elevated}')
            if name == 'clear-utility-with-unexplained-overlay' and any(crit >= 5 for crit in traits.values()):
                raise SystemExit(f'{name}: appended labels asserted hostility')
            print(f'{name}: ok', flush=True)


if __name__ == '__main__':
    main()
