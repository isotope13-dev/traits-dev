"""Distinguish advisory prose from agent consent bypass and SDK identity."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

fixtures = Path(__file__).resolve().parent
root = fixtures.parent.parent
consent = 'objectives/evasion/security-bypass/llm/prompt/override::llm-no-human-consent'
retired = {
    'objectives/exfiltration/http/agent::llm-no-human-consent',
    'objectives/execution/exploit/vulnerability-reference::linux-kernel-cve-reference',
    'objectives/execution/automation/agent::agent-exploit-workflow-marker',
    'objectives/execution/automation/prompt-agent::agent-grant-filesystem',
    'objectives/execution/automation/prompt-agent::agent-grant-credentials',
    'well-known/lib/cloud/azure-identity::package-reference',
}
sdk = 'well-known/lib/cloud/azure-identity::azure-identity-js-sdk'
instruction = 'objectives/execution/automation/prompt-agent::build-artifact-carries-agent-instruction'
mb = 'micro-behaviors/data/llm/agent::'
claims = 'metadata/package/documentation/claims::'
advisory = 'metadata/package/documentation/security-advisory::'
cases = {
    'dom-model.json': (set(), {consent}),
    'data-model.txt': (set(), {consent}),
    'agent-consent.txt': ({consent}, set()),
    'assistant-consent.txt': ({consent}, set()),
    'ai-model-consent.txt': ({consent}, set()),
    'consent-guardrail.txt': (set(), {consent}),
    'advisory.json': ({advisory + 'linux-kernel-cve-reference',
                       advisory + 'exploit-workflow-wording',
                       claims + 'filesystem-access-wording',
                       claims + 'credential-access-grant-wording'}, {consent, instruction}),
    'agent-instruction.js': ({instruction, mb + 'agent-role-assignment-prompt',
                              claims + 'filesystem-access-wording',
                              claims + 'cloud-access-grant-wording',
                              claims + 'credential-access-grant-wording'}, set()),
    'azure-reference.json': ({'metadata/package/documentation/claims::azure-identity-package-reference'}, {sdk}),
    'azure-sdk.js': ({sdk}, set()),
}


def check_case(item):
    name, (required, forbidden) = item
    # Scan outside testdata so path-based fixture exclusions cannot mask errors.
    with tempfile.TemporaryDirectory(prefix='feed-drift-controls-') as directory:
        target = Path(directory) / name
        shutil.copyfile(fixtures / name, target)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
             '--format', 'jsonl', str(target)],
            env={**os.environ, 'CLEAVE_VALIDATE': '0'},
            check=True, capture_output=True, text=True,
        )
        ids = {trait['id'] for line in result.stdout.splitlines()
               for file in json.loads(line).get('files', [])
               for trait in file.get('traits', [])}
        assert required <= ids, (name, 'missing', required - ids, result.stderr)
        assert not (forbidden | retired) & ids, (name, 'unexpected', (forbidden | retired) & ids)
        return name + ' passed'


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(check_case, cases.items()):
        print(result)
