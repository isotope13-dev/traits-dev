"""Static controls for inference boundaries; no specimen code is executed."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PERSIST = 'objectives/persistence/system/init/boot::multi-method-elf-persistence-templates'
OLD_BOOT = 'objectives/persistence/system/init/boot::elf-multi-surface-boot-persistence'
INJECT = 'objectives/lateral-movement/exploit/network-device/http::country-config-shell-substitution'
BOTNAME = 'micro-behaviors/process/info/name::botkill-name-reference'

def elf(strings):
    """Nonexecuting ELF with ordinary section names and a single return opcode."""
    names = b'\0.text\0.rodata\0.shstrtab\0'
    data = b'\0'.join(x.encode() for x in strings) + b'\0'
    ro = 0x100
    shnames = ro + len(data)
    shoff = (shnames + len(names) + 7) & ~7
    b = bytearray(shoff + 4 * 64)
    ident = b'\x7fELF\x02\x01\x01' + bytes(9)
    struct.pack_into('<16sHHIQQQIHHHHHH', b, 0, ident, 2, 62, 1, 0x400080, 64, shoff, 0, 64, 56, 1, 64, 4, 3)
    struct.pack_into('<IIQQQQQQ', b, 64, 1, 5, 0, 0x400000, 0x400000, len(b), len(b), 0x1000)
    b[0x80] = 0xc3
    b[ro:ro+len(data)] = data
    b[shnames:shnames+len(names)] = names
    for idx, args in enumerate([(1, 1, 6, 0x400080, 0x80, 1), (7, 1, 2, 0x400000+ro, ro, len(data)), (15, 3, 0, 0, shnames, len(names))], 1):
        struct.pack_into('<IIQQQQIIQQ', b, shoff+idx*64, *args, 0, 0, 1, 0)
    return b

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    templates = ['[Unit]\nDescription=Example service\n[Service]\nExecStart=/usr/bin/example\nRestart=always\n[Install]\nWantedBy=multi-user.target',
                 '/etc/systemd/system/example.service', '/etc/init.d/example', '### BEGIN INIT INFO', '@reboot /usr/bin/example']
    cases = {
        'service-templates': (templates, set(), {PERSIST, OLD_BOOT, INJECT}),
        'country-injection': (['operation=write&country=$(id)'], {INJECT}, {PERSIST}),
        'android-data-path': (['/data/app/example/base.apk'],
            {'micro-behaviors/fs/path/location::android-app-install-data-path'}, set()),
        'router-data-url': (['/data/user_lang.json'], set(),
            {'micro-behaviors/fs/path/location::android-app-install-data-path',
             'micro-behaviors/fs/path/location::android-app-runtime-path-references'}),
        'country-code': (['operation=write&country=US'], set(), {INJECT}),
        'missing-substitution': (['operation=write&country=(id)'], set(), {INJECT}),
        'botkill-name': (['botkill'], {BOTNAME}, {PERSIST}),
        'robotkill-name': (['robotkill'], set(), {BOTNAME}),
        'service-paths': (['/etc/sv/example/run', '/etc/s6/example/run', '/etc/profile.d/example.sh'],
                          {'micro-behaviors/fs/path/config/system::runit-service-path',
                           'micro-behaviors/fs/path/config/system::s6-service-run-path',
                           'micro-behaviors/fs/path/config/system::system-profiled-path'}, {PERSIST}),
        'service-path-near-miss': (['/tmp/sv/example/run', '/tmp/s6/example/run', '/tmp/profile.d/example.sh'], set(),
                          {'micro-behaviors/fs/path/config/system::runit-service-path',
                           'micro-behaviors/fs/path/config/system::s6-service-run-path',
                           'micro-behaviors/fs/path/config/system::system-profiled-path'}),
    }
    with tempfile.TemporaryDirectory(prefix='fallout-static-controls-') as tmp:
        paths = []
        for name, (strings, _, _) in cases.items():
            p = Path(tmp)/(name+'.elf'); p.write_bytes(elf(strings)); paths.append(str(p))
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'jsonl', *paths], capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr
        reports = {Path(f['path']).stem:f for line in result.stdout.splitlines() for f in json.loads(line)['files']}
        for name, (_, required, absent) in cases.items():
            ts = {t['id']:t['crit'] for t in reports[name].get('traits', [])}
            assert required <= ts.keys(), (name, required-ts.keys())
            assert not absent & ts.keys(), (name, absent & ts.keys())
            assert not any(c == 5 for c in ts.values()), (name, ts)
            if BOTNAME in ts: assert ts[BOTNAME] == 3
        print(f'Passed {len(cases)} nonexecuting positive and near-miss controls.')

if __name__ == '__main__': main()
