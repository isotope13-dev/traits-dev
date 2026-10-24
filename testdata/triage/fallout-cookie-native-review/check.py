#!/usr/bin/env python3
"""Static regression controls; no specimen is ever executed.

Supply the sample root and a scratch directory. Mutated copies are temporary;
the original specimens, existing rules and their coverage are preserved.
"""
import argparse
import json
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RULES = {
    'run': 'objectives/persistence/login/registry/autostart::rolling-xor-run-key-image-transplant-loader',
    'delete': 'objectives/evasion/self-delete/process::rolling-xor-image-loader-batch-cleanup',
    'uac': 'objectives/privilege-escalation/token-manipulation::x86-wusa-filtered-token-uac-bypass',
    'service': 'micro-behaviors/os/service/create::x86-encoded-auto-service-script-format',
    'firewall': 'micro-behaviors/os/firewall/netsh::x86-encoded-netsh-inbound-allow-format',
    'hide': 'objectives/evasion/file-hiding/attributes::hidden-system-persistent-resource-injector',
    'eval': 'objectives/command-and-control/backdoor/webshell/request/eval::php-direct-request-eval-webshell',
}


def offset(blob, va):
    pe = struct.unpack_from('<I', blob, 0x3c)[0]
    count = struct.unpack_from('<H', blob, pe + 6)[0]
    optsize = struct.unpack_from('<H', blob, pe + 20)[0]
    base = struct.unpack_from('<I', blob, pe + 24 + 28)[0]
    for i in range(count):
        sec = pe + 24 + optsize + 40 * i
        size, rva, rawsize, raw = struct.unpack_from('<IIII', blob, sec + 8)
        if rva <= va - base < rva + max(size, rawsize):
            return raw + va - base - rva
    raise AssertionError(hex(va))


def patch(blob, va, old, new):
    assert len(old) == len(new)
    pos = offset(blob, va)
    assert blob[pos:pos + len(old)] == old, (hex(va), blob[pos:pos + len(old)])
    return blob[:pos] + new + blob[pos + len(old):]


def u32(n):
    return struct.pack('<I', n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('samples', type=Path)
    ap.add_argument('scratch', type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    tofsee = (args.samples / '2c7da5333ec8/tofsee.exe').read_bytes()
    storm = (args.samples / '41eda28effa2/2026-10-22_92051c596b94781320fa977c64b5563d_elex_wannacry').read_bytes()
    php = (args.samples / '009277d49048/request-execution.php').read_bytes()
    cases = {}

    def add(name, blob, **expected):
        cases[name] = (blob, expected)

    add('tofsee-original.exe', tofsee, run=True, delete=True, uac=True, service=True, firewall=True)
    add('storm-original.exe', storm, hide=True)
    add('cookie-original.php', php, eval=True)

    # Actual source/API/handle relationships must hold, even if the original
    # encrypted strings and API imports remain elsewhere in the same file.
    add('run-wrong-source.exe', patch(tofsee, 0x409f28, u32(0x4106ac), u32(0x4106e8)), run=False)
    add('run-wrong-open-api.exe', patch(tofsee, 0x409f3d, u32(0x410060), u32(0x410058)), run=False)
    add('run-wrong-write-api.exe', patch(tofsee, 0x409f60, u32(0x410028), u32(0x410058)), run=False)
    add('run-different-hkey.exe', patch(tofsee, 0x409f5d, b'\xec', b'\xe8'), run=False)
    relocated = bytearray(tofsee)
    src, dst = offset(tofsee, 0x4106ac), offset(tofsee, 0x411f00)
    assert not any(relocated[dst:dst + 46])
    relocated[dst:dst + 46] = tofsee[src:src + 46]
    relocated = patch(bytes(relocated), 0x409f28, u32(0x4106ac), u32(0x411f00))
    add('run-relocated-source.exe', relocated, run=True)

    add('delete-wrong-source.exe', patch(tofsee, 0x40918f, u32(0x4107a8), u32(0x410794)), delete=False)
    add('delete-different-image-buffer.exe', patch(tofsee, 0x40917c, u32(0xfffffefc), u32(0xfffffdfc)), delete=False)
    add('delete-wrong-formatter.exe', patch(tofsee, 0x4091ab, u32(0x4101e4), u32(0x4101e8)), delete=False)
    label = bytearray(tofsee)
    # XOR's key schedule is independent of input; relabel both retry targets.
    for i in (12, 79):
        pos = offset(tofsee, 0x4107a8) + i
        label[pos] ^= ord('n') ^ ord('r')
    add('delete-renamed-label.exe', bytes(label), delete=True)

    add('uac-wrong-integrity-class.exe', patch(tofsee, 0x401482, b'\x19', b'\x18'), uac=False)
    add('uac-without-lua-filter.exe', patch(tofsee, 0x4014a1, b'\x04', b'\x00'), uac=False)
    add('uac-thread-hide-not-impersonate.exe', patch(tofsee, 0x4014e3, b'\x05', b'\x11'), uac=False)
    add('uac-wrong-resolved-slot.exe', patch(tofsee, 0x4014a5, u32(0x41394c), u32(0x413950)), uac=False)
    add('uac-wrong-elevated-image.exe', patch(tofsee, 0x40138f, u32(0x41127c), u32(0x411240)), uac=False)
    add('uac-wrong-launch-api.exe', patch(tofsee, 0x40139c, u32(0x4101dc), u32(0x4101d8)), uac=False)
    add('uac-wrong-token-source.exe', patch(tofsee, 0x4013bc, u32(0x413940), u32(0x413944)), uac=False)
    add('uac-without-net-only-logon.exe', patch(tofsee, 0x40161d, b'\x02', b'\x01'), uac=False)
    moved = patch(tofsee, 0x401239, u32(0x41394c), u32(0x4139e0))
    moved = patch(moved, 0x4014a5, u32(0x41394c), u32(0x4139e0))
    add('uac-relocated-resolved-slot.exe', moved, uac=True)

    add('service-wrong-source.exe', patch(tofsee, 0x4093f7, u32(0x410918), u32(0x410888)), service=False)
    add('service-wrong-formatter.exe', patch(tofsee, 0x40940e, u32(0x4101e4), u32(0x4101e8)), service=False)
    changed = bytearray(tofsee)
    changed[offset(tofsee, 0x410918) + 96] ^= ord('a') ^ ord('d')
    add('service-without-auto-start.exe', bytes(changed), service=False)
    changed = bytearray(tofsee)
    changed[offset(tofsee, 0x410918) + 115] ^= 1
    add('service-renamed-display-name.exe', bytes(changed), service=True)

    add('firewall-wrong-source.exe', patch(tofsee, 0x409474, u32(0x410888), u32(0x410918)), firewall=False)
    changed = bytearray(tofsee)
    changed[offset(tofsee, 0x410888) + 94] ^= ord('l') ^ ord('b')
    add('firewall-without-allow.exe', bytes(changed), firewall=False)
    changed = bytearray(tofsee)
    changed[offset(tofsee, 0x410888) + 50] ^= 1
    add('firewall-renamed-rule.exe', bytes(changed), firewall=True)

    add('storm-no-hidden-attributes.exe', patch(storm, 0x402179, b'\x06', b'\x20'), hide=False)
    add('storm-wrong-attribute-api.exe', patch(storm, 0x402183, u32(0x403058), u32(0x40305c)), hide=False)
    # Raw byte tables and API imports, without executable code, are insufficient.
    inert = bytearray(tofsee)
    inert[0x400:0xea00] = bytes(0xe600)
    add('inert-tables-and-imports.exe', bytes(inert), **dict.fromkeys(('run', 'delete', 'uac', 'service', 'firewall'), False))

    for source in ('GET', 'POST', 'REQUEST', 'COOKIE'):
        add(f'php-direct-{source.lower()}.php', f'<?php EvAl /* comment */ ($_'+source+'["x"]);', eval=True)
    php_controls = {
        'comment': '<?php /* eval($_COOKIE["x"]); */ echo "ok";',
        'quoted': '<?php $example = \'eval($_COOKIE["x"]);\'; echo $example;',
        'logged': '<?php error_log(\'eval($_COOKIE["x"]);\');',
        'predicate': '<?php eval(strval(isset($_COOKIE["x"])));',
        'local-eval': '<?php eval("return 1 + 2;"); echo $_COOKIE["x"];',
        'array-local': '<?php $input = ["x" => "return 1;"]; eval($input["x"]);',
        'constant-cookie': '<?php eval($_COOKIE["x"] === "ok" ? "return 1;" : "return 0;");',
    }
    for name, content in php_controls.items():
        add(f'php-{name}.php', content, eval=False)

    args.scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.scratch, prefix='fallout-controls-') as work:
        for name, (content, _) in cases.items():
            (Path(work) / name).write_bytes(content.encode() if isinstance(content, str) else content)
        proc = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json', work],
                              capture_output=True, text=True, check=True)
        assert not proc.stderr.strip(), proc.stderr
        rest, seen, results, failures = proc.stdout, set(), [], []
        decoder = json.JSONDecoder()
        while rest.strip():
            report, length = decoder.raw_decode(rest.lstrip())
            rest = rest.lstrip()[length:]
            for f in report['files']:
                name = Path(f['path']).name
                if name not in cases or 'pid' in f:
                    continue
                actual = {t['id'] for t in f.get('traits', [])}
                for key, expected in cases[name][1].items():
                    if (RULES[key] in actual) != expected:
                        failures.append((name, key, expected))
                seen.add(name)
                results.append({'case': name, 'expected': cases[name][1], 'passed': True})
        assert seen == cases.keys(), (seen, cases.keys())
        assert not failures, failures
    (args.scratch / 'control-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} static controls passed')


if __name__ == '__main__':
    main()
