#!/usr/bin/env python3
"""Exercise linked execution and retained neutral observations outside test paths."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser=argparse.ArgumentParser()
parser.add_argument('--traits',type=Path,default=Path(__file__).resolve().parents[3])
parser.add_argument('--scratch',type=Path,required=True)
parser.add_argument('--baseline',type=Path)
args=parser.parse_args()
fixtures=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='three-script-controls-',dir=args.scratch) as tmp:
    root=Path(tmp)
    for file in fixtures.iterdir():
        if file.suffix in ('.py','.bat') and file.name not in ('check.py','trace.py'):
            shutil.copyfile(file,root/file.name)
    # Include independent, pre-existing positive and benign fixtures.
    for name,source in {
        'existing-settra.bat':'testdata/hostile/settra-chain.bat',
        'existing-recovery.bat':'testdata/hostile/recovery-disable.bat',
        'existing-traversal.py':'testdata/hostile/urllib-put-traversal-drop.py',
        'sitecustomize.py':'testdata/benign/litellm-4098-startup/sitecustomize.py',
    }.items(): shutil.copyfile(args.traits/source,root/name)
    def scan(traits):
        result=subprocess.run(['cleave','--traits-dir',str(traits),'--format','json','analyze',str(root)],capture_output=True,text=True)
        if result.returncode: raise RuntimeError(result.stderr)
        remaining=result.stdout; decoder=json.JSONDecoder(); reports={}
        while remaining.strip():
            value,end=decoder.raw_decode(remaining.lstrip());remaining=remaining.lstrip()[end:]
            for file in value['files']: reports[Path(file['path']).name]=file
        return reports
    after=scan(args.traits)
    before=scan(args.baseline) if args.baseline else {}
    def ids(name): return {t['id'] for t in after[name].get('traits',[])}
    poll='objectives/command-and-control/remote-command/http-poll::python-urllib-fork-loop-exec'
    startup='objectives/persistence/system/python-startup::startup-hook-urllib-code-daemon'
    drop='objectives/command-and-control/channel/deaddrop/url::python-urllib-detached-response-host-tasking'
    token='objectives/credential-access/cloud/token/oauth::password-spray-retains-refresh-token-records'
    note='objectives/impact/ransom/note::recovery-destruction-with-lock-contact-note'
    for name in ('loader.py','loader-renamed.py'): assert {poll,startup,drop}<=ids(name),name
    for name in ('loader-overwritten.py','loader-different-handle.py','loader-unrelated-loop.py','loader-local-file.py','loader-direct-overwritten.py','sitecustomize.py'):
        assert not {poll,startup,drop}&ids(name),name
    assert poll in ids('loader-direct.py')
    assert poll in ids('loader-fixed-host.py') and drop not in ids('loader-fixed-host.py')
    assert {poll,drop}<=ids('loader-no-startup.py') and startup not in ids('loader-no-startup.py')
    assert token in ids('spray.py')
    for name in ('single-auth.py','spray-no-token-record.py','spray-different-token-record.py','spray-overwritten-token.py'): assert token not in ids(name),name
    assert note in ids('existing-settra.bat')
    assert 'micro-behaviors/fs/write/file/redirect::batch-file-lock-contact-note-write' not in ids('echo-name-nearmiss.bat')
    for name in ('maintenance.bat','support-note.bat','existing-recovery.bat'):
        assert note not in ids(name),name
    assert 'micro-behaviors/fs/disk/partition::diskpart-script-file' in ids('maintenance.bat')
    assert 'micro-behaviors/network/dns::flushdns-quiet-command' in ids('maintenance.bat')
    assert 'micro-behaviors/os/event/log::defender-operational-log-channel' in ids('maintenance.bat')
    moves={
        'objectives/impact/wipe/disk/orchestration::diskpart-script-file':'micro-behaviors/fs/disk/partition::diskpart-script-file',
        'objectives/impact/wipe/disk/orchestration::diskpart-script-recovery-inhibition':'objectives/impact/ransom/recovery-inhibition::winre-disable-diskpart-with-trace-destruction',
        'objectives/evasion/anti-av/blinding::defender-operational-log-channel':'micro-behaviors/os/event/log::defender-operational-log-channel',
        'objectives/evasion/indicator-removal/cleanup::flushdns-quiet-command':'micro-behaviors/network/dns::flushdns-quiet-command',
    }
    changes={}
    for name,report in before.items():
        old={moves.get(t['id'],t['id']) for t in report.get('traits',[])}
        changes[name]={'lost':sorted(old-ids(name)),'gained':sorted(ids(name)-old)}
    # Wrong data bindings/local URLs/unrelated loops intentionally lose the
    # former co-occurrence-based remote-code-daemon conviction. Real loader,
    # external traversal and recovery fixtures retain all supported findings.
    for name in ('loader.py','loader-renamed.py','loader-direct.py','existing-settra.bat','existing-recovery.bat','existing-traversal.py','sitecustomize.py'):
        if name in changes: assert not changes[name]['lost'],(name,changes[name]['lost'])
    (args.scratch/'focused-results.json').write_text(json.dumps({'cases':len(after),'changes':changes},indent=2)+'\n')
    print(f'{len(after)} cases passed; independent attack coverage retained')
