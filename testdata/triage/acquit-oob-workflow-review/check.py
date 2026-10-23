"""Focused static controls; no fixture or network operation is executed."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[3]
append = 'micro-behaviors/fs/write/file/append::shell-heredoc-append-redirection'
post = 'micro-behaviors/communications/http/post::python-collect-post'
axios = 'micro-behaviors/communications/http/request/body::axios-data-request-literal'
b64 = 'micro-behaviors/data/encode/base64::json-field-btoa-value'
retired = {
    'micro-behaviors/communications/http/upload::python-collect-post',
    'micro-behaviors/communications/http/post::axios-with-data',
    'micro-behaviors/communications/http/request/body::json-field-btoa-value',
}

def decode_many(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, end = decoder.raw_decode(text)
        yield report
        text = text[end:]

with tempfile.TemporaryDirectory(prefix='acquit-controls-', dir=Path(__file__).parent) as work:
    cases = []
    def case(name, content, required=(), absent=()):
        path = Path(work) / name
        path.write_text(content)
        cases.append((path, set(required), set(absent)))

    case('append.sh', 'cat >> "$REPORT" <<\'END\'\nstatus: ready\nEND\n', [append])
    case('overwrite.sh', 'cat > "$REPORT" <<\'END\'\nstatus: ready\nEND\n', absent=[append])
    case('string-only.sh', 'echo \'cat >> "$REPORT" <<END\'\n', absent=[append])
    case('no-heredoc.sh', 'echo ready >> "$REPORT"\n', absent=[append])
    case('collection.py', 'import requests\nrequests.post("https://api.vendor.invalid/collect", json={"status":"ready"})\n', [post])
    case('comment.py', '# requests.post("https://api.vendor.invalid/collect", json={"status":"ready"})\n', absent=[post])
    case('other-path.py', 'import requests\nrequests.post("https://api.vendor.invalid/metrics", json={"status":"ready"})\n', absent=[post])
    case('axios-literal.js', 'const example = "axios({method: \'GET\', data: payload})";\n', [axios])
    case('axios-no-data.js', 'const example = "axios({method: \'GET\'})";\n', absent=[axios])
    case('json-base64.js', 'const record = JSON.stringify({value: btoa(input)});\n', [b64])
    case('json-plain.js', 'const record = JSON.stringify({value: input});\n', absent=[b64])
    cases += [
        (repo/'testdata/hostile/supply-chain-controls/import-time-oob-beacon.py', {
            'objectives/exfiltration/oob/endpoint::python-oob-json-post',
            'objectives/supply-chain/recon-exfil/import-time::import-time-host-profile-beacon',
            'objectives/supply-chain/recon-exfil/import-time::import-time-oob-host-profile-beacon', post}, set()),
        (repo/'testdata/hostile/supply-chain-corpus/gha/gha-marrowworks-workflow-inject-linux.tgz', {
            'objectives/supply-chain/trojanized/ci-pipeline::action-cache-gated-workflow-shell-implant',
            'objectives/supply-chain/trojanized/ci-pipeline::cache-gated-workflow-shell-append', append}, set()),
    ]
    proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo), '--format', 'json', *[str(c[0]) for c in cases]],
                          capture_output=True, text=True, check=True, timeout=300)
    reports = list(decode_many(proc.stdout))
    assert len(reports) == len(cases), (len(reports), len(cases))
    for (path, required, absent), report in zip(cases, reports):
        traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
        assert required <= traits.keys(), (path.name, required-traits.keys())
        assert not (retired | absent) & traits.keys(), (path.name, (retired|absent)&traits.keys())
        if append in traits:
            assert traits[append] == 3
        print(path.name + ': PASS')
    print(str(len(cases)) + ' focused cases passed')
