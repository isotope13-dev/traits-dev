#!/usr/bin/env python3
"""Verify endpoint-review findings using inert samples and generated controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--inventory', required=True)
p.add_argument('--atomscan', default='../scan/target/release/atomscan')
p.add_argument('--output', required=True)
a = p.parse_args()
rows = json.loads(Path(a.inventory).read_text())
if isinstance(rows, dict):
    rows = rows['samples']

def sample(prefix):
    row = next(s for s in rows if s['sha256'].startswith(prefix))
    data = Path(row.get('local_path', row['path'])).read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256']
    return data

publish = 'objectives/impact/spam::postinstall-random-disposable-package-publish'
template = 'micro-behaviors/fs/write/file/target::postinstall-random-name-manifest-template'
copy = 'micro-behaviors/os/kernel/device::intel-kernel-copy-request-call'
physical = 'micro-behaviors/os/kernel/device::intel-physical-map-request-call'
cases = []
with tempfile.TemporaryDirectory(prefix='endpoint-reassessment-controls-') as temporary:
    tmp = Path(temporary)

    def add(name, data, yes=None, no=(), ceiling=None):
        path = tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode() if isinstance(data, str) else data)
        cases.append((path, yes or {}, set(no), ceiling))

    hooks = []
    for prefix, version in [('9f22a7', '19'), ('14d2fb', '22')]:
        data = sample(prefix)
        archive = tmp / ('probe-' + version + '.tgz')
        archive.write_bytes(data)
        with tarfile.open(archive) as tar:
            metadata = json.load(tar.extractfile('package/package.json'))
        hook = metadata['scripts']['postinstall']
        hooks.append(hook)
        add('original-' + version + '/package.json', json.dumps(metadata), {publish: 5, template: 3})
    hook = hooks[0]

    def manifest(name, value, yes=None, no=(), script='postinstall'):
        add(name + '/package.json', json.dumps({'name': 'control', 'version': '1.0.0',
            'scripts': {script: value}}), yes, no)

    manifest('renamed', hook.replace('publish-poc-found-', 'different-').replace('$d', '$stage'), {publish: 5})
    manifest('short-flag', hook.replace('--hex', '-hex'), {publish: 5})
    manifest('no-cleanup', hook.replace('; rm -rf $d', ''), {template: 3}, (publish,))
    manifest('fixed-name', hook.replace('publish-poc-found-%s', 'fixed-artifact'), no=(publish, template))
    manifest('release-only', hook, no=(publish, template), script='prepublishOnly')
    manifest('no-publish', hook.replace('npm publish $d', 'echo $d'), no=(publish,))
    manifest('random-description', hook.replace('"$(openssl rand --hex 2)" "$contents"',
        '"$contents" "$(openssl rand --hex 2)"'), no=(publish, template))
    m = {'name':'control', 'version':'1.0.0', 'scripts': {'postinstall': hook.replace(
        '"$(openssl rand --hex 2)"', '"$release_name"'), 'test':'openssl rand --hex 2'}}
    add('unrelated-randomness/package.json', json.dumps(m), no=(publish, template))
    add('inert-prose/package.json', json.dumps({'name':'control','version':'1.0.0','description':hook}), no=(publish, template))

    native = sample('c1c295')
    add('kernel-client.exe', native, {copy: 4, physical: 4})
    # Locate instruction blocks by bytes instead of collector names or offsets.
    ioctl = bytes.fromhex('ba07208680')
    assert native.count(ioctl) >= 4
    add('different-ioctl.exe', native.replace(ioctl, bytes.fromhex('ba08208680')), no=(copy, physical))
    selector = bytes.fromhex('49c743c033000000ff15')
    assert selector in native
    add('different-copy-selector.exe', native.replace(selector, bytes.fromhex('49c743c034000000ff15')), {physical: 4}, (copy,))
    selector = bytes.fromhex('48c745ef19000000')
    assert selector in native
    add('different-map-selector.exe', native.replace(selector, bytes.fromhex('48c745ef18000000')), {copy: 4}, (physical,))
    # Extract just the signed vendor driver by the independently recorded span.
    driver = native[0x148600:0x148600 + 97168]
    # Derive its raw PE extent without importing or executing the driver.
    import struct
    peoff = struct.unpack_from('<I', driver, 0x3c)[0]
    count = struct.unpack_from('<H', driver, peoff + 6)[0]
    optional = struct.unpack_from('<H', driver, peoff + 20)[0]
    sec = peoff + 24 + optional
    extent = max(struct.unpack_from('<I', driver, sec + i*40 + 20)[0] +
                 struct.unpack_from('<I', driver, sec + i*40 + 16)[0] for i in range(count))
    add('vendor-driver.sys', driver[:extent], no=(copy, physical))

    scan = subprocess.run([a.atomscan, '--no-update', '--mode', 'slow', '--format',
        'json', 'path'] + [str(c[0]) for c in cases], capture_output=True, text=True,
        env=dict(os.environ, CLEAVE_TRAITS_DIR=str(Path.cwd()), XDG_CACHE_HOME=str(tmp/'cache')))
    assert scan.returncode in (0,1), scan.stderr
    observed = {}
    for line in scan.stdout.splitlines():
        files = json.loads(line)['raw']['files']
        observed[files[0]['path']] = {t['id']:t['crit'] for f in files for t in f.get('traits',[])}
    assert len(observed) == len(cases), (len(observed), len(cases), scan.stderr)
    report = []
    for path, yes, no, ceiling in cases:
        traits = observed[str(path)]
        assert all(traits.get(k) == v for k,v in yes.items()), (str(path),yes,traits)
        assert not no.intersection(traits), (str(path),no.intersection(traits))
        if ceiling is not None:
            assert max(traits.values(),default=0) <= ceiling
        report.append({'case':str(path.relative_to(tmp)), 'required':yes,
                       'forbidden':sorted(no),'passed':True})
    Path(a.output).write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(report)} endpoint-review boundaries passed')
