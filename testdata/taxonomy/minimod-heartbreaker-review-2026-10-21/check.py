"""Statically scan attack fixtures and near misses; execute no sample code."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
base = Path(__file__).resolve().parent
paths = [base / 'encrypted-replacement.rs',
         root / 'testdata/hostile/fabric-obfuscated-abi-account-loader.jar',
         root / 'testdata/hostile/jvm-native-browser-collector.jar']
r = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json',
                    *map(str, paths)], capture_output=True, text=True, check=True)
decoder = json.JSONDecoder()
remaining = r.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files.update({f['path']: f for f in report['files']})
for p in paths:
    traits = files[str(p)]['traits']
    ids = {t['id'] for t in traits}
    if p.name == 'encrypted-replacement.rs':
        assert 'micro-behaviors/fs/write/encrypted::aead-overwrite-rename-profile' in ids
        assert ('objectives/anti-static/obfuscation/payload/polymorphic/generator'
                '::embedded-rust-source-mutation') in ids
        assert not any(t['crit'] == 5 for t in traits)
    elif p.name == 'fabric-obfuscated-abi-account-loader.jar':
        assert 'objectives/credential-access/gaming/minecraft::minecraft-token-jar-handoff' in ids
        assert 'objectives/execution/payload/module-load::minecraft-token-abi-jar-loader' in ids
        assert sum(t['crit'] == 5 for t in traits) >= 3
    else:
        assert 'objectives/exfiltration/stealer/browser::jvm-native-browser-collector-multipart-upload' in ids
        assert sum(t['crit'] == 5 for t in traits) >= 3
    assert 'objectives/exfiltration/stealer/token::minecraft-named-token-tls-post' not in ids
    print('PASS', p.name)
