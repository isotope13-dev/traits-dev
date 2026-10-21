"""Check neutral .github writes and retained install-hook reporting coverage.

The two source fixtures are unmodified published files, never executed:
  lisa-remote-aws.mjs: @codyswann/lisa 4.81.8, plugins/src/base/scripts/
                     install-remote-agent-aws.mjs (also identical in 4.81.7).
  registry-reporter.cjs: @lystech/core 3.0.126, bin/postinstall.cjs.

Usage: python3 testdata/lisa-workflow-write/verify.py <scratch-directory>
"""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent
WRITE = 'micro-behaviors/fs/write/file/target::node-writes-github-config-path'
OLD = ('objectives/supply-chain/install-hook/project-rewrite::'
       'postinstall-writes-consumer-github-workflow')
REPORT = ('objectives/supply-chain/install-hook/project-rewrite::'
          'npm-postinstall-package-registry-workflow-beacon')


def scan(paths):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'jsonl', *map(str, paths)],
        text=True, capture_output=True, check=True)
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    return {Path(report['files'][0]['path']).name:
            {t['id']: t['crit'] for f in report['files'] for t in f['traits']}
            for report in reports}


def archive(dest, source, hook=True):
    manifest = {'name': 'workflow-control', 'version': '1.0.0'}
    if hook:
        manifest['scripts'] = {'postinstall': 'node bin/postinstall.cjs'}
    with tarfile.open(dest, 'w:gz') as out:
        for name, data in [('package/package.json', json.dumps(manifest)),
                           ('package/bin/postinstall.cjs', source)]:
            encoded = data.encode()
            entry = tarfile.TarInfo(name)
            entry.size = len(encoded)
            out.addfile(entry, io.BytesIO(encoded))
    return dest


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    cases = {
        'direct.js': ("fs.writeFileSync('.github/workflows/ci.yml', body);", True),
        'renamed.js': (
            "const dir = path.join(root, '.github', 'workflows');\n"
            "const output = path.join(dir, 'ci.yml');\n"
            "fs.writeFileSync(output, body);", True),
        'other-github-config.js': (
            "writeFileSync(path.resolve(root, '.github', 'CODEOWNERS'), body);", True),
        'unrelated-variable.js': (
            "const workflowPath = '/tmp/report.json';\n"
            "fs.writeFileSync(workflowPath, body);", False),
        'unrelated-path.js': (
            "const reference = '.github/workflows/ci.yml';\n"
            "fs.writeFileSync('/tmp/report.json', body);", False),
        'read-only.js': (
            "fs.readFileSync('.github/workflows/ci.yml', 'utf8');", False),
        'comment-only.js': (
            "// fs.writeFileSync('.github/workflows/ci.yml', body);", False),
        'opaque-transform.js': (
            "fs.writeFileSync(unknown('.github/workflows/ci.yml'), body);", False),
        'lisa-remote-aws.mjs': ((FIXTURES / 'lisa-remote-aws.mjs').read_text(), True),
    }
    reporter = (FIXTURES / 'registry-reporter.cjs').read_text()
    # The original detector accidentally depended on this freely chosen name.
    cases['renamed-reporter.cjs'] = (reporter.replace('workflowPath', 'output'), True)
    targets = []
    expectations = {}
    for name, (source, expected) in cases.items():
        target = scratch / name
        target.write_text(source)
        targets.append(target)
        expectations[name] = (expected, False)
    for name, source, hook, expected in [
        ('original-report.tgz', reporter, True, True),
        ('renamed-report.tgz', reporter.replace('workflowPath', 'output'), True, True),
        ('no-hook.tgz', reporter, False, False),
        ('no-report.tgz', reporter.replace('api/package-registry', 'health'), True, False),
        ('local-write.tgz', reporter.replace('".github"', '"local"'), True, False),
    ]:
        targets.append(archive(scratch / name, source, hook))
        expectations[name] = (None, expected)
    reports = scan(targets)
    assert set(reports) == set(expectations), reports.keys()
    for name, (write_expected, expected) in expectations.items():
        ids = reports[name]
        if write_expected is not None:
            assert (WRITE in ids) == write_expected, (name, ids)
        if WRITE in ids:
            assert ids[WRITE] in (3, 'notable'), (name, ids[WRITE])
        assert (REPORT in ids) == expected, (name, ids)
        assert OLD not in ids, (name, 'retired false claim')
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
