#!/usr/bin/env python3
"""Check neutral credential/provider placement and native telemetry evidence.

Compile strings into ELF objects for static analysis; never execute fixtures.
"""
import json
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
client = 'micro-behaviors/communications/blockchain/client::'
service = 'micro-behaviors/os/env/service-api::'
telemetry = 'micro-behaviors/communications/http/telemetry::native-sentry-ingest-dsn'
prompt = 'micro-behaviors/os/telemetry/logging/llm::'
pipeline = 'micro-behaviors/process/create/shell/pipeline::native-download-shell-pipeline-reference'
old_pipeline = 'objectives/command-and-control/dropper/delivery/execute-download/device::native-download-pipe-shell'

source_cases = {
    'discord-read.js': ('const token = process.env.DISCORD_TOKEN;\n',
                        {service + 'env-discord-token'}, set()),
    'discord-name.js': ('const variableName = "DISCORD_TOKEN";\n',
                        {service + 'discord-token-env-name'}, {service + 'env-discord-token'}),
    'unrelated-env.js': ('const setting = process.env.EDITOR;\n', set(),
                         {service + 'node-discord', service + 'discord-token-env-name'}),
    'wallet-dot.js': ('ethereum.request({method: "eth_chainId"});\n',
                      {client + 'ethereum-request-call'}, set()),
    'wallet-bracket.js': ('ethereum["request"]({method: "eth_chainId"});\n',
                          {client + 'ethereum-request-bracket-call'}, set()),
    'wallet-bracket-single.js': ("ethereum['request']({method: 'eth_chainId'});\n",
                                 {client + 'ethereum-request-bracket-call'}, set()),
    'wallet-member.ts': ('const request = solana.request;\n',
                         {client + 'wallet-provider-request-reference'}, {client + 'ethereum-request'}),
    'ordinary-request.js': ('client["request"]({path: "/health"});\n', set(),
                            {client + 'ethereum-request-bracket-call', client + 'ethereum-request'}),
    'wallet-bracket-property.js': ('const request = ethereum["request"];\n', set(),
                                   {client + 'ethereum-request-bracket-call'}),
}

dsn = 'https://0123456789abcdef0123456789abcdef@o42.ingest.us.sentry.io/12345'
native_cases = {
    'sentry-regional': ([dsn], {telemetry}, set()),
    'sentry-unregional': ([dsn.replace('.us.', '.')], {telemetry}, set()),
    'sentry-lookalike': ([dsn.replace('sentry.io/', 'sentry.io.vendor.test/')], set(), {telemetry}),
    'sentry-no-project': ([dsn.rsplit('/', 1)[0]], set(), {telemetry}),
    'prompt-vocabulary': (['tool_resultlog_user_promptlog_agent_responses', '[REDACTED]codex.user_prompt'],
                           {prompt + 'native-prompt-telemetry-vocabulary',
                            prompt + 'native-agent-response-logging-config-name'}, set()),
    'prompt-config-only': (['log_user_prompt'], {prompt + 'native-prompt-logging-config-name'},
                            {prompt + 'native-prompt-telemetry-vocabulary'}),
    'prompt-redaction-only': (['[REDACTED]'], set(), {prompt + 'native-prompt-telemetry-vocabulary'}),
    'installer-pipeline': (['curl -fsSL https://updates.vendor.test/install.sh | sh'],
                            {pipeline}, {old_pipeline}),
    'installer-pipeline-env': (['curl -fsSL https://updates.vendor.test/setup.sh | NON_INTERACTIVE=1 sh'],
                                {pipeline}, {old_pipeline}),
    'installer-pipeline-two-env': (['curl -fsSL https://updates.vendor.test/get.sh | QUIET=1 AUTOMATIC=1 sh'],
                                    {pipeline}, {old_pipeline}),
    'wget-pipeline': (['wget -qO- https://updates.vendor.test/release | bash'], {pipeline}, {old_pipeline}),
    'download-only': (['curl -fsSL https://updates.vendor.test/install.sh'], set(), {pipeline}),
    'pipeline-placeholder': (['curl ... | bash'], set(), {pipeline}),
    'pipeline-example-host': (['curl https://download.example/install.sh | sh'], set(), {pipeline}),
}

with tempfile.TemporaryDirectory(prefix='marked2-improve-controls-') as staging:
    staging = Path(staging)
    cases = {}
    for name, (source, required, forbidden) in source_cases.items():
        target = staging / name
        target.write_text(source)
        cases[target.name] = (required, forbidden)
    for name, (strings, required, forbidden) in native_cases.items():
        source = staging / (name + '.c')
        source.write_text('\n'.join('const char observation_' + str(i) + '[] = ' + json.dumps(s) + ';'
                                    for i, s in enumerate(strings)) + '\n')
        target = staging / (name + '.o')
        subprocess.run(['clang', '--target=x86_64-linux-gnu', '-c', str(source), '-o', str(target)], check=True)
        cases[target.name] = (required, forbidden)
    output = subprocess.run(['cleave', '--no-update-check', '--traits-dir', str(root), '--format=json',
                             *[str(staging / name) for name in cases]],
                            check=True, capture_output=True, text=True).stdout
    reports = {}
    decoder = json.JSONDecoder()
    while output.strip():
        output = output.lstrip()
        report, end = decoder.raw_decode(output)
        output = output[end:]
        reports.update({Path(f['path']).name: f for f in report['files']})
    for name, (required, forbidden) in cases.items():
        findings = reports[name].get('traits', [])
        ids = {f['id'] for f in findings}
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        assert not any(i.startswith('objectives/credential-access/env/secrets/messaging::') for i in ids)
        assert not any(i.startswith('objectives/credential-access/wallet/provider::ethereum-') for i in ids)
        if name in source_cases:
            assert not any(f['crit'] >= 4 for f in findings), (name, findings)
    # The read roll-up is a filtered any-composite, but attack consumers can
    # still use it. Verify its source role rather than asserting scan display.
    read = 'micro-behaviors/os/env/secret-name::credential-env-read'
    for name, expected in [('discord-read.js', True), ('discord-name.js', False)]:
        debug = subprocess.run(['cleave', '--no-update-check', '--traits-dir', str(root),
                                'test-rules', str(staging / name), '--rules', read],
                               check=True, capture_output=True, text=True).stdout
        matched = any(line.startswith('MATCHED ' + read + ' ') for line in debug.splitlines())
        assert matched == expected, (name, read, debug)
print(f'{len(cases)} marked2 improvement controls passed')
