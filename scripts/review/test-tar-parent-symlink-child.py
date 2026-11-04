#!/usr/bin/env python3
"""Detect a tar member under a root symlink that points above extraction."""
import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import zipfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
cases = {'escape.tar': ('foo', '../', 'foo/bar'),
         'renamed.tar': ('different', '../outside', 'different/data'),
         'safe-link.tar': ('foo', 'inside', 'foo/bar'),
         'other-child.tar': ('foo', '../', 'other/bar'),
         'deep-link.tar': ('dir/foo', '../', 'dir/foo/bar')}
with tempfile.TemporaryDirectory(prefix='tar-symlink-test-') as temp:
    root = Path(temp)
    for name, (link, target, child) in cases.items():
        with tarfile.open(root / name, 'w', format=tarfile.USTAR_FORMAT) as tf:
            entry = tarfile.TarInfo(link)
            entry.type = tarfile.SYMTYPE
            entry.linkname = target
            tf.addfile(entry)
            entry = tarfile.TarInfo(child)
            data = b'hello'
            entry.size = len(data)
            tf.addfile(entry, io.BytesIO(data))
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases)],
                       check=True, capture_output=True, text=True,
                       env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    trait = 'objectives/execution/exploit/symlink::tar-root-parent-symlink-child-payload'
    assert trait in found['escape.tar'] and trait in found['renamed.tar']
    assert all(trait not in found[n] for n in ('safe-link.tar', 'other-child.tar', 'deep-link.tar'))
    harness = '''otherStream.pipe(tar.extract(out))
test('do not extract invalid tar', function (t) {
  var a = path.join(__dirname, 'fixtures', 'invalid.tar')
  var out = path.join(__dirname, 'fixtures', 'invalid')
  fs.createReadStream(a).pipe(tar.extract(out)).on('error', function (err) {
    fs.stat(path.join(out, '../bar'), function (err) { t.ok(err) })
  })
})
'''
    archives = []
    for name, fixture, code in [('positive.zip', 'escape.tar', harness),
                                ('safe.zip', 'safe-link.tar', harness),
                                ('no-harness.zip', 'escape.tar', 'ordinary code'),
                                ('wrong-name.zip', 'escape.tar', harness)]:
        dest = root / name
        with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('package/test/index.js', code)
            member = 'other.tar' if name == 'wrong-name.zip' else 'invalid.tar'
            z.write(root / fixture, 'package/test/fixtures/' + member)
        archives.append(dest)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(x) for x in archives)],
                       check=True, capture_output=True, text=True,
                       env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    harness_trait = 'objectives/execution/exploit/path-traversal::tar-fs-parent-escape-regression-poc'
    assert harness_trait in found['positive.zip'], found['positive.zip']
    assert all(harness_trait not in found[n] for n in ('safe.zip', 'no-harness.zip', 'wrong-name.zip'))
    print('Tar symlink payload requires a root escape and a descendant entry.')
