"""Check claim placement, hidden activation, archive scope, and retained attacks."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
p.add_argument('--scratch', required=True)
a = p.parse_args()
root = Path(__file__).resolve().parents[3]
fixture = Path(__file__).resolve().parent

def decode_reports(text):
    decoder = json.JSONDecoder()
    files = []
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        files.extend(report['files'])
    return {f['path']: {t['id']: t['crit'] for t in f.get('traits', [])} for f in files}

with tempfile.TemporaryDirectory(prefix='registry-review-', dir=a.scratch) as d:
    work = Path(d)
    source = (fixture / 'shortcode.php.fixture').read_text()
    for name in ['worker-status.html', 'package.json']:
        (work / name).write_bytes((fixture / name).read_bytes())
    for name, data in {
        'plugin.php': source,
        'renamed.php': source.replace('/tmp/.bc9782', '/tmp/.different'),
        'ordinary.php': source.replace('eval("?>" . $body);', 'echo $body;'),
        'unconditional.php': source.replace('if (!file_exists("/tmp/.bc9782")) {\n        return "";\n    }', ''),
        'inline.sh': "ruby -e 'require \"base64\"; eval(Base64.decode64(ARGV[0]))' ZWNobyBoaQ==\n",
        'syntax.sh': "printf '%s' 'eval(value)'\n",
        'invoice.pdf.hta': '<html><body>Document</body></html>',
        'invoice.hta': '<html><body>Document</body></html>',
    }.items():
        (work / name).write_text(data)
    with zipfile.ZipFile(work / 'split.zip', 'w') as z:
        z.writestr('local.php', '<?php add_shortcode("local", function() { eval("echo 1;"); });')
        z.writestr('fetch.php', '<?php wp_remote_get("https://service.invalid/"); $p="/tmp/.cache";')
    inputs = [str(x) for x in work.iterdir()]
    r = subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'json', *inputs], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    files = decode_reports(r.stdout)
    direct = 'micro-behaviors/process/interpreter/eval/direct::wp-shortcode-eval-hook'
    remote = 'objectives/command-and-control/backdoor/webshell/wordpress::wordpress-shortcode-remote-eval'
    gate = 'objectives/execution/trigger/plugin::hidden-file-guarded-shortcode-remote-eval'
    guard = 'micro-behaviors/fs/file/stat::hidden-tmp-absent-return-guard'
    for name in ['plugin.php', 'renamed.php']:
        got = files[str(work / name)]
        assert got[remote] == 5 and got[direct] == 4 and got[gate] == 4 and got[guard] == 3, (name, got)
    got = files[str(work / 'ordinary.php')]
    assert got[guard] == 3 and remote not in got and gate not in got, got
    got = files[str(work / 'unconditional.php')]
    assert guard not in got and gate not in got, got
    assert all(remote not in traits for path, traits in files.items() if 'split.zip' in path)
    for name in ['worker-status.html', 'package.json']:
        got = files[str(work / name)]
        assert not any(c == 5 for c in got.values()), (name, got)
    got = files[str(work / 'worker-status.html')]
    assert got['micro-behaviors/ui/window/visibility::hidden-iframe-near-executable-query'] == 3
    assert got['micro-behaviors/process/create/workers::inert-worker-near-executable-query'] == 3
    got = files[str(work / 'package.json')]
    assert got['metadata/package/dependencies/direct-url::url-dependency-with-install-hooks'] == 3
    assert got['metadata/package/dependencies/direct-url::runtime-and-dev-plaintext-http-dependencies'] == 4
    syntax = 'metadata/lang/source/syntax/call/invocation::workflow-eval-call-text'
    assert syntax in files[str(work / 'syntax.sh')]
    assert files[str(work / 'inline.sh')]['objectives/anti-static/obfuscation/payload/encoded/exec::inline-ruby-base64-eval'] == 5
    suffix = 'metadata/file/extension/executable::pdf-double-extension-script'
    assert suffix in files[str(work / 'invoice.pdf.hta')]
    assert suffix not in files[str(work / 'invoice.hta')]
    print('PASS: shortcode execution/guard, split archive, status Worker, HTTP dependencies, Ruby consumer, PDF suffix')
