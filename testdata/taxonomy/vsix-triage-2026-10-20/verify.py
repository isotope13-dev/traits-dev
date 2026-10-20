#!/usr/bin/env python3
"""Check VSIX techniques and benign controls without running extension code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BRIDGE = 'objectives/command-and-control/reverse-shell/stream-bridge::node-socket-callback-shell-bridge'
ENCODED = 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-hidden-encoded-executable-stage'
PAIR = 'objectives/command-and-control/dropper/staging/native/payload::batch-temp-native-pair-background-stage'
PROFILE = 'objectives/exfiltration/stealer/system-info/profile::base64-env-profile-fetch-query'
STARTUP = 'objectives/supply-chain/recon-exfil/callback::vscode-startup-encoded-profile-query'
VULNERABLE = 'objectives/supply-chain/trojanized/app/ai-agent-tools::prompt-requests-vulnerable-code'
CASES = {
    'auth-identity-poc.vsix': {'require': ['objectives/credential-access/dev-tools/session::serializer-extension-identity-rewrite', 'objectives/credential-access/dev-tools/session::silent-auth-session-with-identity-rewrite'], 'suspicious_min': 2, 'hostile_max': 0},
    'ordinary-silent-session.js': {'criticality_max': 3},
    'ordinary-identity-migration.js': {'criticality_max': 3},
    'socket-shell.vsix': {'require': [BRIDGE], 'hostile_min': 3},
    'encoded-downloader.vsix': {'require': [ENCODED], 'hostile_min': 1},
    'native-pair.vsix': {'require': [PAIR, 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-hidden-batch-native-pair-stage'], 'suspicious_min': 2},
    'profile-beacon.vsix': {'require': [PROFILE, STARTUP], 'suspicious_min': 2, 'hostile_max': 0},
    'security-policy.vsix': {'criticality_max': 3},
    'disclosed-provider.vsix': {'criticality_max': 3},
    'notification-helper.vsix': {'criticality_max': 3},
    'socket-client.js': {'criticality_max': 3},
    'unrelated-streams.js': {'criticality_max': 3},
    'powershell-helper.js': {'criticality_max': 3},
    'ordinary-download.bat': {'hostile_max': 0, 'forbid': [PAIR]},
    'rejected-code-request.js': {'criticality_max': 3},
    'live-code-request.js': {'require': [VULNERABLE]},
    'mixed-code-request.js': {'require': [VULNERABLE]},
    'offline-xor-profile.js': {'criticality_max': 3},
}
engine = os.environ.get('CLEAVE', str(REPO.parent / 'cleave/target/release/cleave'))
result = subprocess.run([engine, '--traits-dir', str(REPO), '--format', 'json', *[str(HERE / name) for name in CASES]], capture_output=True, text=True, check=True, timeout=600)
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files = report.get('files', [])
    if files:
        reports[Path(files[0]['path']).name] = files
errors = []
for name, expected in CASES.items():
    files = reports.get(name)
    if files is None:
        errors.append(f'{name}: missing report')
        continue
    findings = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
    root = {t['id']: t['crit'] for t in files[0].get('traits', [])}
    high = {k: v for k, v in findings.items() if v >= 4}
    for rule in expected.get('require', []):
        if rule not in findings:
            errors.append(f'{name}: missing {rule}')
    for rule in expected.get('forbid', []):
        if rule in findings:
            errors.append(f'{name}: unexpected {rule}')
    for level, crit in [('hostile', 5), ('suspicious', 4)]:
        count = sum(value >= crit for value in root.values())
        if count < expected.get(level + '_min', 0) or count > expected.get(level + '_max', float('inf')):
            errors.append(f'{name}: {level} count {count}')
    if max(findings.values(), default=0) > expected.get('criticality_max', 5):
        errors.append(f'{name}: unexpected high findings {high}')
    print(f'{name}: {len(high)} suspicious/hostile traits')
assert not errors, '\n'.join(errors)
print(f'PASS: {len(CASES)} cases')
