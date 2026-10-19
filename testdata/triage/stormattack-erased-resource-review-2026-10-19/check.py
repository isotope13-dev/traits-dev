"""Offline scan controls. Usage: python3 check.py OUTER_SAMPLE SCRATCH_DIR.

Only read and mutate bytes; never load or execute the PE samples.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
WRITE = 'micro-behaviors/os/registry/write::servicedll-registry-write-api-cluster'
OLD = 'micro-behaviors/os/service/create::servicedll-registry-write-api-cluster'
PATH = 'micro-behaviors/fs/path/system::system32-executable-path'
SYSTEM = 'micro-behaviors/fs/path/system::windows-system-directory'
CREATE = 'micro-behaviors/os/service/create::create-service'


def main():
    sample, scratch = map(Path, sys.argv[1:3])
    work = scratch / 'stormattack-erased-controls'
    work.mkdir(parents=True, exist_ok=True)
    original = sample.read_bytes()
    expected = {}
    for name, token, present in [
        ('no-create-service.exe', b'CreateServiceA', True),
        ('no-servicedll.exe', b'ServiceDLL', False),
        ('no-registry-writer.exe', b'RegSetValueExA', False),
    ]:
        assert token in original
        (work / name).write_bytes(original.replace(token, b'X' * len(token)))
        expected[name] = {WRITE: present, OLD: False}
        if name == 'no-create-service.exe':
            expected[name][CREATE] = False
    for name, path, image, system in [
        ('system32-dll.ps1', r'C:\Windows\System32\srvsvc.dll', True, False),
        ('system32-exe.ps1', r'C:\Windows\System32\cmd.exe', True, False),
        ('system32-driver.ps1', r'C:\Windows\System32\drivers\example.sys', True, False),
        ('escaped-system32.ps1', r'C:\\Windows\\System32\\slui.exe', False, False),
        ('system-directory.ps1', r'C:\Windows\System\example.dll', False, True),
        ('system32-nonimage.ps1', r'C:\Windows\System32\example.txt', False, False),
    ]:
        (work / name).write_text('$p = "' + path + '"\n')
        expected[name] = {PATH: image, SYSTEM: system}
    result = subprocess.run(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'jsonl', str(work)],
        text=True, capture_output=True, check=True)
    (scratch / 'stormattack-erased-controls.json').write_text(result.stdout)
    reports = [json.loads(line) for line in result.stdout.splitlines() if line]
    checked = []
    entries = [entry for report in reports for entry in report['files']]
    for entry in entries:
        name = Path(entry['path']).name
        if name not in expected:
            continue
        traits = {item['id']: item for item in entry['traits']}
        for rule, present in expected[name].items():
            assert (rule in traits) == present, (name, rule, present)
        if PATH in traits:
            assert traits[PATH]['crit'] == 3, (name, 'path must remain notable')
        checked.append(name)
    assert set(checked) == set(expected), checked
    print('PASS: 9 registry-placement and path-boundary controls')


if __name__ == '__main__':
    main()
