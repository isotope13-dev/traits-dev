#!/usr/bin/env python3
"""Scan synthetic ELF controls as data; never execute the generated files."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def elf(symbol, permissions, strings):
    # One resolved mprotect syscall plus exit. A symbol table gives the name
    # matcher a real function, independently of any quoted string in .rodata.
    code = bytes.fromhex('31ffbe00100000ba') + struct.pack('<I', permissions)
    code += bytes.fromhex('b80a0000000f0531ffb83c0000000f05')
    data = bytearray(0x100)
    code_offset = len(data)
    data += code
    ro_offset = len(data)
    rodata = b'\x07\0\0\0' * 8 + b'\0'.join(s.encode() for s in strings) + b'\0'
    data += rodata
    data += b'\0' * (-len(data) % 8)
    strtab = b'\0' + symbol.encode() + b'\0'
    sym_offset = len(data)
    data += bytes(24) + struct.pack('<IBBHQQ', 1, 0x12, 0, 1, 0x400000 + code_offset, len(code))
    str_offset = len(data)
    data += strtab
    names = b'\0.text\0.rodata\0.symtab\0.strtab\0.shstrtab\0'
    names_offset = len(data)
    data += names
    data += b'\0' * (-len(data) % 8)
    sh_offset = len(data)
    sections = [bytes(64)]
    for name, kind, flags, addr, offset, size, link, info, align, entsize in [
        ('.text', 1, 6, 0x400000 + code_offset, code_offset, len(code), 0, 0, 16, 0),
        ('.rodata', 1, 2, 0x400000 + ro_offset, ro_offset, len(rodata), 0, 0, 1, 0),
        ('.symtab', 2, 0, 0, sym_offset, 48, 4, 1, 8, 24),
        ('.strtab', 3, 0, 0, str_offset, len(strtab), 0, 0, 1, 0),
        ('.shstrtab', 3, 0, 0, names_offset, len(names), 0, 0, 1, 0),
    ]:
        sections.append(struct.pack('<IIQQQQIIQQ', names.index(name.encode()), kind, flags,
                                    addr, offset, size, link, info, align, entsize))
    data += b''.join(sections)
    ident = b'\x7fELF\x02\x01\x01' + bytes(9)
    data[:64] = struct.pack('<16sHHIQQQIHHHHHH', ident, 2, 62, 1,
                           0x400000 + code_offset, 64, sh_offset, 0, 64, 56, 1, 64, 6, 5)
    data[64:120] = struct.pack('<IIQQQQQQ', 1, 5, 0, 0x400000, 0x400000, len(data), len(data), 0x1000)
    return data


def main():
    with tempfile.TemporaryDirectory(prefix='triage-evidence-') as tmp:
        root = Path(tmp)
        (root / 'diagnostics.elf').write_bytes(elf('SSL_CTX_set_dos_protection_cb', 3, [
            'No escaped character', 'Failed to unlink cache temporary file after creation.',
            'privatekey', 'is_file', 'try -threads 1', '_read_cmd_output', 'Buffered data will be lost.',
        ]))
        (root / 'operations.elf').write_bytes(elf('udp_flood', 7, [
            'There is no escape', 'unlink /var/log/messages', 'Usage: scanner [target] [port]',
        ]))
        (root / 'hash.elf').write_bytes(elf('BKDRHash', 3, []))
        (root / 'named-handler.elf').write_bytes(elf('bd_handler_dispatch', 3, []))
        result = subprocess.run([
            os.environ.get('ATOMSCAN', 'atomscan'), '--no-update', '--mode', 'slow',
            '--format', 'json', 'path', str(root / 'diagnostics.elf'), str(root / 'operations.elf'),
            str(root / 'hash.elf'), str(root / 'named-handler.elf'),
        ], cwd=ROOT, env=dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_ANALYSIS_MEMO_MB='0'),
            text=True, capture_output=True)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        assert 'Failed to parse YAML' not in result.stderr, result.stderr
        findings = {}
        for line in result.stdout.splitlines():
            report = json.loads(line)['raw']['files'][0]
            findings[Path(report['path']).name] = {t['id'] for t in report.get('traits', [])}
        assert set(findings) == {'diagnostics.elf', 'operations.elf', 'hash.elf', 'named-handler.elf'}, result.stderr
        naming = 'objectives/evasion/masquerade/naming/posix::backdoor-keywords'
        assert naming not in findings['hash.elf']
        assert naming in findings['named-handler.elf']
        benign, positive = findings['diagnostics.elf'], findings['operations.elf']
        differentiators = {
            'micro-behaviors/mem/protect/modify::mprotect-rwx-syscall',
            'objectives/impact/dos/udp::flood-function-symbol',
            'objectives/impact/ui/manipulation/lockscreen-keywords::no-escape-phrase',
            'objectives/impact/wipe/logs::native-log-wipe-unlink-command',
        }
        assert not benign & differentiators, benign & differentiators
        assert differentiators <= positive, differentiators - positive
        expected = {
            'micro-behaviors/crypto/asymmetric/key::privatekey-identifier',
            'micro-behaviors/fs/file/stat::is-file-identifier',
            'micro-behaviors/process/thread/config::thread-count-cli-option',
            'micro-behaviors/ui/dialog/error::data-loss-warning',
        }
        assert expected <= benign, expected - benign
        assert 'micro-behaviors/ui/help::bracketed-parameter-usage' in positive
        assert all('repeated-07-byte-constant' not in trait for traits in findings.values() for trait in traits)
        print('Passed: syscall permissions, TLS DoS protection, escape diagnostics, log unlink, neutral identifiers, backdoor/hash naming')


if __name__ == '__main__':
    main()
