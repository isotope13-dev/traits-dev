"""Check security-disable prompts with inert PE controls and the real sample."""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AV = 'objectives/evasion/anti-av/dialog::antivirus-blocking-disable-restart-prompt'
SAC = 'objectives/impact/degrade/windows-policy::smart-app-control-off-restart-prompt'
SPEC = importlib.util.spec_from_file_location(
    'pe_fixture', ROOT / 'testdata/triage-sighted/build_pe_fixtures.py')
fixture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixture)


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--sample', type=Path)
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    av = ('Your anti-virus is preventing ExampleApp from loading a dependency. '
          'Please disable it and restart ExampleApp.')
    sac = ('Smart App Control is blocking renamed_plugin.dll from loading '
           'because it is unsigned. Go to Windows Security > App & browser '
           'control > Smart App Control settings and turn Smart App Control '
           'Off, then restart ExampleApp.')
    cases = {
        'both.exe': (av + '\0' + sac, {AV, SAC}),
        'av-only.exe': (av, {AV}),
        'sac-only.exe': (sac, {SAC}),
        'renamed-uppercase.exe': (
            (av.replace('ExampleApp', 'AnotherTool') + '\0' +
             sac.replace('renamed_plugin.dll', 'other_module.bin')).upper(),
            {AV, SAC}),
        'av-enable.exe': (av.replace('disable it', 'enable it'), set()),
        'av-keep-enabled.exe': (
            av.replace('Please disable it', 'Do not disable it'), set()),
        'av-status-only.exe': (av.split('. Please')[0], set()),
        'sac-enable.exe': (sac.replace('Control Off', 'Control On'), set()),
        'sac-keep-enabled.exe': (
            sac.replace('settings and turn', 'settings and do not turn'), set()),
        'sac-status-only.exe': (sac.split('. Go')[0], set()),
        'unrelated-ui.exe': ('Open a Lua script\0LoadLibraryExW\0'
                             'GetAsyncKeyState\0Smart App Control', set()),
        # Unrelated strings must not bridge a native string terminator.
        'split-av.exe': (av.replace('. Please', '.\0Please'), set()),
        'split-sac.exe': (sac.replace('settings and turn', 'settings and\0turn'), set()),
    }
    expected = {}
    for name, (payload, wanted) in cases.items():
        path = args.work_dir / name
        path.write_bytes(fixture.image(b'.rdata', payload.encode() + b'\0', 4096))
        expected[str(path)] = wanted
    command = [args.cleave, '--traits-dir', str(ROOT), '--disable',
               'yara,radare2,upx', '--format', 'json', str(args.work_dir)]
    if args.sample:
        command.append(str(args.sample))
        expected[str(args.sample)] = {AV, SAC}
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    seen = set()
    for report in reports(result.stdout):
        for entry in report['files']:
            path = entry['path']
            if path not in expected:
                continue
            actual = {t['id'] for t in entry.get('traits', [])} & {AV, SAC}
            assert actual == expected[path], (path, actual, expected[path])
            seen.add(path)
    assert seen == set(expected), ('missing reports', set(expected) - seen)
    print(f'PASS: {len(seen)} prompt controls/sample reports')


if __name__ == '__main__':
    main()
