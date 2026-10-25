"""Static matcher controls; sample code is never executed."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = {
    'tunna-reference.py': ([
        'metadata/lang/source/naming/target::tunna-name-reference',
    ], []),
    'tun-interface.go': ([], [
        'metadata/lang/source/naming/target::tunna-name-reference',
    ]),
    'neutral.go': ([
        'metadata/lang/source/naming/resource::go-module-path-name-reference',
        'micro-behaviors/data/control-flow/loop::go-incrementing-port-loop',
        'micro-behaviors/crypto/certificate/extensions::go-authentication-extended-key-usages',
        'micro-behaviors/communications/dns/lookup::go-lookup-netip-call',
        'micro-behaviors/process/io/stream::go-tokenization-command-output-cooccurrence',
    ], [
        'metadata/lang/source/syntax/key-value::go-times-numeric-field',
        'objectives/discovery/network/scan/port/probe::network-scanner',
        'objectives/discovery/network/scan/port/probe::scan-operations',
        'objectives/evasion/process/injection/module-stomping::module-stomping-config',
    ]),
    'secure-delete.go': ([
        'metadata/lang/source/syntax/key-value::go-times-numeric-field',
        'objectives/evasion/indicator-removal/cleanup::go-secure-shred-pattern',
        'micro-behaviors/fs/delete/secure::secure-file-deletion',
    ], []),
    'scanner.go': ([
        'micro-behaviors/data/control-flow/loop::go-incrementing-port-loop',
        'objectives/discovery/network/scan/port/probe::network-scanner',
    ], []),
    'template.js': ([
        'metadata/lang/source/literal::pass-prefixed-source-line',
        'metadata/lang/source/literal::protocol-version-string-literal',
        'metadata/lang/source/naming/action::update-check-helper-name-reference',
    ], [
        'micro-behaviors/communications/irc/command::password-command-template',
        'micro-behaviors/communications/mcp::mcp-protocol-version-field',
        'micro-behaviors/os/package-manager/upgrade::npm-registry-self-update-check-marker',
    ]),
    'healthkit.swift': ([
        'micro-behaviors/data/db/query::swift-healthkit-sample-query',
        'micro-behaviors/data/db/query::swift-healthkit-statistics-query',
        'micro-behaviors/data/db/query::swift-healthkit-anchored-query',
    ], []),
    'healthkit-mentions.swift': ([], [
        'micro-behaviors/data/db/query::swift-healthkit-sample-query',
        'micro-behaviors/data/db/query::swift-healthkit-statistics-query',
        'micro-behaviors/data/db/query::swift-healthkit-anchored-query',
        'micro-behaviors/hardware/input/audio::swift-avaudio-recorder-construction',
    ]),
    'service-setup.sh': ([
        'micro-behaviors/os/kernel/driver::shell-insmod-path',
        'micro-behaviors/os/kernel/driver::shell-insmod-ko',
        'micro-behaviors/os/service/configure::openrc-add-service-command',
        'micro-behaviors/os/service/configure::systemctl-enable-trigger-unit',
        'metadata/lang/source/syntax/command::tailscale-memory-state-option',
        'metadata/lang/source/syntax/command::tailscale-no-logs-option',
    ], []),
}

command = [os.environ.get('CLEAVE', 'cleave'), '--no-update-check', '--traits-dir', str(ROOT), '--format', 'json']
command += [str(HERE / name) for name in CASES]
result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
remaining = result.stdout.strip()
reports = []
while remaining:
    report, consumed = json.JSONDecoder().raw_decode(remaining)
    reports.extend(report['files'])
    remaining = remaining[consumed:].strip()
by_name = {Path(report['path']).name: report for report in reports}
for name, (required, absent) in CASES.items():
    traits = {t['id']: t for t in by_name[name].get('traits', [])}
    assert set(required) <= traits.keys(), (name, set(required) - traits.keys(), result.stderr)
    assert not set(absent) & traits.keys(), (name, set(absent) & traits.keys())
    for ident in required:
        assert traits[ident]['crit'] >= 3, (name, ident)
    print('PASS', name)
