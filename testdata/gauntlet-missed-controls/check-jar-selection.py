"""Verify the JAR selector on an externally supplied specimen; never execute it."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', required=True)
parser.add_argument('--sample', required=True, type=Path)
parser.add_argument('--reports', required=True, type=Path)
args = parser.parse_args()
assert args.sample.stat().st_size > 1024 * 1024, 'Disk-path control requires a JAR larger than 1 MiB'
repo = Path(__file__).resolve().parents[2]
args.reports.mkdir(parents=True, exist_ok=True)
required = {
    'micro-behaviors/communications/tls/verify/disable::java-trust-all-x509trustmanager',
    'objectives/evasion/security-bypass/tls::java-tls-client-own-trust-all-manager',
    'objectives/command-and-control/dropper/file-exec/spawn::java-trustall-png-archive-process-stager',
    'objectives/supply-chain/trojanized/app/game-mod::fabric-net-fabric-png-trustall-stager',
}
env = dict(os.environ, CLEAVE_NO_UPDATE_CHECK='1', XDG_CACHE_HOME='/tmp/gauntlet-cache',
           RAYON_NUM_THREADS='2')
for memory_mb in (100, 1):
    run = subprocess.run([args.cleave, '--traits-dir', str(repo), '--max-file-mem',
                          str(memory_mb), '--format=json', 'analyze', str(args.sample)],
                         env=env, capture_output=True, text=True, check=True, timeout=240)
    report = json.loads(run.stdout)
    traits = {trait['id'] for file in report['files'] for trait in file.get('traits', [])}
    assert required <= traits, (memory_mb, required - traits)
    assert any(file['path'].endswith('net/fabric/hqulgIdi$lhkIdx.class')
               for file in report['files']), 'Trust-manager companion must be retained'
    (args.reports / f'ikea-memory-{memory_mb}.json').write_text(run.stdout)
    print(f'PASS JAR max-file-mem={memory_mb}: companion, TLS nest, both hostile stager findings', flush=True)
