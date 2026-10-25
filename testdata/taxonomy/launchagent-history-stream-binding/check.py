"""Exercise actual source/stream bindings without executing the C# fixtures."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).parent
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json', str(fixtures)],
    check=True, capture_output=True, text=True, timeout=180)
# cleave may concatenate report objects without adding line separators.
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
seen = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report['files']:
        seen[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}

prefix = 'objectives/exfiltration/stealer/file::'
for name in ['bound-post.cs', 'renamed-bound-post.cs']:
    assert prefix + 'csharp-history-post-shell-job' in seen[name], name
    assert prefix + 'launchagent-history-stream-post' in seen[name], name
for name in ['unrelated-stream.cs', 'unrelated-file.cs', 'reassigned-stream.cs', 'local-agent.cs']:
    assert prefix + 'csharp-history-post-shell-job' not in seen[name], name
    assert prefix + 'launchagent-history-stream-post' not in seen[name], name
    assert 'objectives/persistence/system/launchd/source::source-launchagent-remote-shell-persistence' not in seen[name], name
print('PASS: two bound transfers and four boundary controls')
