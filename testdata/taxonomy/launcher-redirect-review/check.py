"""Static regression controls. Generated PE entry points are never executed.

Run: python3 check.py SCRATCH_DIR [ORIGINAL_LAUNCHER]
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'pe_controls', ROOT / 'testdata/taxonomy/managed-tuner-observations/check.py')
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)
NAV = 'micro-behaviors/ui/window/navigation::instant-refresh-wordpress-admin-disk-image'
MOVED = 'micro-behaviors/process/interpreter/runtime/clr::appdomain-unsigned-filename-mismatch'
OLD = 'micro-behaviors/metaprogramming/reflection::appdomain-unsigned-filename-mismatch'
TOKENS = {
    b'OpenSubKey': 'micro-behaviors/os/registry/access::dotnet-open-subkey-reference',
    b'FileStream': 'micro-behaviors/fs/file/open::dotnet-filestream-type-reference',
    b'set_SecurityProtocol': 'micro-behaviors/communications/tls/initialize::dotnet-security-protocol-setter-reference',
    b'get_BaseDirectory': 'micro-behaviors/process/info/selfpath::dotnet-base-directory-getter-reference',
}


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    redirect = '<meta http-equiv="Refresh" content="0; url=https://files.example.org/wp-admin/assets/release.iso" />'
    html_cases = [
        ('admin-image.html', redirect, {NAV}, set()),
        ('admin-image-case.html', redirect.upper(), {NAV}, set()),
        ('normal-image.html', redirect.replace('/wp-admin/', '/downloads/'), set(), {NAV}),
        ('delayed-image.html', redirect.replace('"0;', '"10;'), set(), {NAV}),
        ('comment-image.html', '<!--' + redirect + '-->', set(), {NAV}),
        ('image-suffix.html', redirect.replace('.iso"', '.iso.html"'), set(), {NAV}),
        ('separate-link.html', '<meta http-equiv="Refresh" content="0; url=https://files.example.org/" /><a href="https://files.example.org/wp-admin/assets/release.iso">image</a>', set(), {NAV}),
        ('plain-link.html', '<a href="https://files.example.org/wp-admin/assets/release.iso">Download</a>', set(), {NAV}),
        ('firewall.html', '<html><script>window.location="/app.js?jdfwkey=9876";</script><a href="/app.js?jdfwkey=9876">Continue</a></html>', set(), {NAV}),
    ]
    cases = [(n, v.encode(), yes, no) for n, v, yes, no in html_cases]
    names = b'\0'.join(TOKENS) + b'\0'
    cases += [
        ('api-names.exe', controls.pe(names), set(TOKENS.values()), set()),
        ('api-suffixes.exe', controls.pe(b'\0'.join(n+b'Example' for n in TOKENS)+b'\0'), set(), set(TOKENS.values())),
        ('resource-names.exe', controls.pe(resource=names), set(), set(TOKENS.values())),
    ]
    if len(sys.argv) > 2:
        data = Path(sys.argv[2]).read_bytes()
        cases += [
            ('renamed-game.bin', data, {MOVED, *TOKENS.values()}, {OLD}),
            ('GemsCloudLauncher.exe', data, set(TOKENS.values()), {MOVED, OLD}),
            ('without-appdomain.bin', data.replace(b'AppDomain\0', b'AppDomaiX\0'), set(TOKENS.values()), {MOVED, OLD}),
        ]
    for name, data, _, _ in cases:
        (scratch / name).write_bytes(data)
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', 'analyze', *[str(scratch / c[0]) for c in cases],
    ], check=True, text=True, capture_output=True)
    decoder, offset, reports = json.JSONDecoder(), 0, {}
    while offset < len(result.stdout):
        while offset < len(result.stdout) and result.stdout[offset].isspace():
            offset += 1
        if offset == len(result.stdout):
            break
        report, offset = decoder.raw_decode(result.stdout, offset)
        for file in report['files']:
            reports[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
    output = []
    for name, _, required, forbidden in cases:
        observed = reports[name]
        assert required <= observed and not forbidden & observed, (name, required-observed, forbidden & observed)
        output.append({'case': name, 'passed': True})
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
