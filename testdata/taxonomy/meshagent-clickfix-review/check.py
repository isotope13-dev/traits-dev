"""Static-only regression checks. Supply original and upstream PE paths."""
import argparse
import json
import pathlib
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--agent', type=pathlib.Path, required=True)
parser.add_argument('--upstream-agent', type=pathlib.Path, required=True)
parser.add_argument('--scratch', type=pathlib.Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
here = pathlib.Path(__file__).resolve().parent
eval_id = 'objectives/execution/payload/script-eval::shell-aes-stage-eval-with-variable-command'
aes_id = 'objectives/execution/payload/script-eval::shell-concealed-hex-aes-stage-eval'
chain_id = 'micro-behaviors/process/deploy/file-exec::variable-output-move-clear-mode-launch-chain'
stage_ids = {
    'objectives/command-and-control/dropper/delivery/fetch-exec::printf-hidden-payload-execution',
    'objectives/evasion/anti-av/platform/gatekeeper::encoded-stager-clears-attributes',
    'objectives/command-and-control/beacon/network/http::pasted-event-payload-beacon',
}
brand_id = 'objectives/evasion/masquerade/version-resource/claim::meshagent-edge-version-masquerade'
service_id = 'objectives/persistence/system/service/install::meshagent-browser-disguised-service'
channel_id = 'objectives/command-and-control/channel/websocket::browser-disguised-meshagent-controller'
pe_ids = {brand_id, service_id, channel_id}
cert_id = 'micro-behaviors/crypto/certificate/usage::cert-create-self-sign'
old_cert = 'objectives/evasion/security-bypass/cert-store::cert-create-self-sign'
upper_id = 'metadata/lang/source/syntax/assignment::shell-uppercase-path-assignment'
default_id = 'metadata/lang/source/syntax/assignment::shell-uppercase-parameter-default'
cases = []


def case(name, data, required=(), forbidden=()):
    path = args.scratch / name
    path.write_bytes(data.encode() if isinstance(data, str) else data)
    cases.append((path, set(required), set(forbidden)))


s1 = (here / 'stage1.zsh').read_text()
s2 = (here / 'stage2.zsh').read_text()
case('stage1.zsh', s1, {eval_id, aes_id}, {upper_id, default_id})
case('concat-decoder.zsh', s1.replace('${xswd9} enc', '${prefix}${suffix} enc'), {eval_id, aes_id})
case('data-only.zsh', s1.replace('eval "$_r"', 'printf "%s" "$_r"'), (), {eval_id, aes_id})
case('unrelated-eval.zsh', s1.replace('eval "$_r"', 'eval "$other"'), (), {eval_id, aes_id})
case('overwritten-eval.zsh', s1.replace('eval "$_r"', '_r="echo harmless"\neval "$_r"'), (), {eval_id, aes_id})
case('stage2.zsh', s2, stage_ids | {chain_id})
case('wrong-launch.zsh', s2.replace('&& ${ib3497}\n', '&& ${unrelated}\n'), (), stage_ids | {chain_id})
case('wrong-move-source.zsh', s2.replace('mv ${kzzdla}', 'mv ${unrelated}'), (), stage_ids | {chain_id})
case('wrong-clear.zsh', s2.replace('-c ${ib3497}', '-c ${unrelated}'), (), stage_ids | {chain_id})
case('wrong-chmod.zsh', s2.replace('+x ${ib3497}', '+x ${unrelated}'), (), stage_ids | {chain_id})
# Retain the original no-move/no-telemetry activation shape used by consumers.
prefix = s2[:s2.index('${pqxmm} -fsSL -o')]
legacy = prefix + '${pqxmm} -o ${ib3497} ${u0pcvc} && ${tkg6b} -c ${ib3497} && ${klr9h} +x ${ib3497} && ${ib3497}\n'
case('legacy-chain.zsh', legacy, stage_ids, {chain_id})
case('uppercase-wrapper.sh', '#!/bin/sh\nDIFF="/usr/bin/diff"\nset -- "$@"\n$DIFF "$@"\n', {upper_id}, {aes_id})
case('uppercase-default.sh', '#!/bin/sh\n: ${DIFF:=diff}\n$DIFF "$@"\n', {default_id}, {aes_id})
case('lowercase-wrapper.sh', '#!/bin/sh\nhelper="/tmp/helper"\n: ${other:=0}\n', (), {upper_id, default_id})
case('lowercase-reconstruction.sh', '#!/bin/sh\nb="/tmp/job"\nset -- sh -c "$b"\n$b "$@"\n',
     {'objectives/anti-static/obfuscation/code-metrics/structure::sh-staged-command-reconstruction'}, {upper_id, default_id})

pe = args.agent.read_bytes()
up = args.upstream_agent.read_bytes()
case('agent.exe', pe, pe_ids | {cert_id}, {old_cert})
case('upstream.exe', up, {cert_id}, pe_ids | {old_cert})
# Byte-preserving ablations retain executable code; these are controls, not
# reconstructions of an original upstream or campaign artifact.
resource_restored = pe.replace('msedge.exe'.encode('utf-16le'), 'agentx.exe'.encode('utf-16le'))
case('no-browser-resource.exe', resource_restored, {service_id, cert_id}, {brand_id, channel_id})
service_restored = pe.replace(b'meshServiceName=MicrosoftEdge', b'meshServiceName=ServiceAgentX').replace(
    b'displayName=Microsoft Edge', b'displayName=CorporateAgent')
case('no-browser-service.exe', service_restored, {brand_id, channel_id, cert_id}, {service_id})
case('no-disguise.exe', service_restored.replace('msedge.exe'.encode('utf-16le'), 'agentx.exe'.encode('utf-16le')),
     {cert_id}, pe_ids)
case('renamed-controller.exe', pe.replace(b'mesh.buttruyen.com:443', b'control.unit.test:443'), pe_ids | {cert_id})

result = subprocess.run([args.cleave, '--traits-dir', '.', '--format', 'jsonl', str(args.scratch)],
                        capture_output=True, text=True)
if result.returncode:
    print(result.stderr, file=sys.stderr)
    result.check_returncode()
(args.scratch.parent / 'controls.scan.jsonl').write_text(result.stdout)
files = [f for line in result.stdout.splitlines() if line.strip()
         for f in json.loads(line)['files']]
by_path = {f['path']: {t['id'] for t in f.get('traits', [])} for f in files}
checks = []
for path, required, forbidden in cases:
    ids = by_path[str(path)]
    missing, unexpected = required - ids, forbidden & ids
    checks.append({'case': path.name, 'missing': sorted(missing), 'unexpected': sorted(unexpected)})
print(json.dumps(checks, indent=2))
assert all(not c['missing'] and not c['unexpected'] for c in checks), 'Regression check failed'
print(f'{len(checks)} static checks passed')
