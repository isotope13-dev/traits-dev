#!/usr/bin/env python3
"""Static regression checks; never execute the PowerShell/Ruby specimens."""
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '/usr/local/var/cyclotron/cleave/target/release/cleave')
FIX = ROOT / 'testdata/hostile/generated/rex-shellcode-policy'
SHELL = 'objectives/execution/payload/memory-branch/shellcode::'
AMSI = 'objectives/evasion/anti-av/amsi::amsi-reflection-init-flag-tampering'
POLICY = 'objectives/evasion/indicator-removal/audit::powershell-scriptblock-policy-cache-disable'
RC4 = 'micro-behaviors/crypto/symmetric/stream/rc4/transform::powershell-rc4-like-state-xor-loop'
RECIPE = 'metadata/build/package/recipe/gemspec::ruby-gem-specification-or-build-reference'
cases = []

def case(name, code, rule, expected=True, suffix='.ps1'):
    cases.append((name + suffix, code, rule, expected))

def rename(code):
    # Render the format placeholders without relying on their original names.
    names = {}
    def render(match):
        name = match.group(1)
        if name.startswith('b64'): return 'AQIDBA=='
        return names.setdefault(name, 'renamed_' + str(len(names)))
    return re.sub(r'%\{(\w+)\}', render, code)

for name, rule in [('dotnet', 'powershell-decoded-buffer-protect-thread'),
                   ('old', 'powershell-rwx-buffer-thread'),
                   ('pshreflection', 'powershell-decoded-buffer-delegate-thread'),
                   ('msil', 'powershell-decoded-msil-method-overwrite')]:
    code = (FIX / (name + '.ps1')).read_text()
    case(name, code, SHELL + rule)
    case(name + '-renamed', rename(code).replace('0x11112222', '34321'), SHELL + rule)
    if name != 'msil':
        target = {'dotnet': '$%{var_baseaddr}', 'old': '$%{var_rwx}',
                  'pshreflection': '$%{var_buffer}'}[name]
        # Only the last occurrence in the thread call is changed. A separate
        # callback must not make an unrelated copied buffer executable.
        pos = code.index('::CreateThread(') if name != 'pshreflection' else code.index('kernel32.dll CreateThread)')
        tail = code[pos:]
        assert target in tail
        wrong = code[:pos] + tail.replace(target, '$separate_callback', 1)
        case(name + '-separate-callback', wrong, SHELL + rule, False)
        case(name + '-no-copy', code.replace('::Copy(', '::ReadByte('), SHELL + rule, False)
        # A direct pointer alias still carries the copied code to the entry.
        line_start = code.rfind('\n', 0, pos) + 1
        alias = code[:line_start] + '$entryAlias = [IntPtr]' + target + '\n' + code[line_start:pos] + tail.replace(target, '$entryAlias', 1)
        case(name + '-pointer-alias', alias, SHELL + rule)
        case(name + '-multiline', code.replace('::Copy(', '::Copy(\n').replace('::CreateThread(', '::CreateThread(\n'), SHELL + rule)

    else:
        case('msil-no-activation', code.rsplit('$%{var_tgt_meth}.Invoke', 1)[0], SHELL + rule, False)

dotnet = (FIX / 'dotnet.ps1').read_text()
for flag in ['0x20', '16', '32', '64', '128']:
    case('execute-' + flag, dotnet.replace('[%{var_kernel32}.func+MemoryProtection]::Execute', flag),
         SHELL + 'powershell-decoded-buffer-protect-thread')
case('utf16-base64-loader', 'powershell -NoP -EncodedCommand ' + base64.b64encode(rename(dotnet).encode('utf-16le')).decode(),
     SHELL + 'powershell-decoded-buffer-protect-thread')
case('nonexecutable-protection', dotnet.replace('[%{var_kernel32}.func+MemoryProtection]::Execute', '0x04'),
     SHELL + 'powershell-decoded-buffer-protect-thread', False)
case('ordinary-byte-copy', '''$d = [Convert]::FromBase64String('AQID')
$p = [Native]::VirtualAlloc(0, 128, 0x3000, 0x04)
[Runtime.InteropServices.Marshal]::Copy($d,0,$p,$d.Length)
[Native]::CreateThread(0,0,$separate_callback,0,0,0)
''', SHELL + 'powershell-decoded-buffer-protect-thread', False)

generator = (FIX / 'policy-generator.rb').read_text()
case('ruby-amsi', generator, AMSI, suffix='.rb')
case('ruby-logging', generator, POLICY, suffix='.rb')
changed = generator
for a, b in [('GPF','cacheField'),('GPC','settings'),('SBL','policyName'),('EnableSBL','loggingFlag'),('EnableSBIL','invocationFlag')]:
    changed = re.sub(r'\$' + a + r'\b', '$' + b, changed)
changed = changed.replace('bypass_amsi', 'emit_one').replace('bypass_script_log', 'emit_two')
case('ruby-renamed-amsi', changed, AMSI, suffix='.rb')
case('ruby-renamed-logging', changed, POLICY, suffix='.rb')
case('ruby-amsi-reenabled', generator.replace('.SetValue($null,$true)', '.SetValue($null,$false)'), AMSI, False, '.rb')
case('ruby-logging-enabled', generator.replace(']=0;', ']=1;'), POLICY, False, '.rb')
case('ruby-unrelated-policy-writes', generator.replace('[$EnableSBL]=0', "['OtherPolicy']=0"), POLICY, False, '.rb')
ps = "$t=[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils');\n"
case('direct-amsi', ps + "$t.GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)", AMSI)
case('multiline-amsi', ps + "$t.GetField(\n'amsiInitFailed',\n'NonPublic,Static').SetValue($null,$true)", AMSI)
case('bound-field-amsi', ps + "$flag=$t.GetField('amsiInitFailed','NonPublic,Static')\n$flag.SetValue($null,$true)", AMSI)
case('unrelated-static-write', ps + "$t.GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$false)\n$other.SetValue($null,$true)", AMSI, False)
case('reflection-inspection', ps + "$t.GetField('amsiInitFailed','NonPublic,Static').GetValue($null)", AMSI, False)
case('policy-inspection', generator.replace(']=0;', ']=1;') + "\n$other['First']=0; $other['Second']=0\n", POLICY, False, '.rb')

stream = (ROOT / 'testdata/notable/generated/rex-rc4-stream/stream.ps1').read_text()
case('rc4-template', stream, RC4)
case('rc4-renamed', rename(stream).replace('$s[', '$state[').replace('$i', '$left').replace('$j', '$right').replace('%%', '%'), RC4)
case('non-byte-state', stream.replace('256', '255'), RC4, False)
case('no-keystream-xor', stream.replace('-bxor', '-bor'), RC4, False)
case('ordinary-xor', '$buffer[$x] = $buffer[$x] -bxor $mask[$x]', RC4, False)

case('ordinary-gemspec', "Gem::Specification.new do |s|\n s.name='release-tool'\nend", RECIPE, suffix='.rb')
case('registry-upload-regression', "Gem::Specification.new\nFile.binwrite('out', data)\nDir.pwd\nputs 'gem push out.gem'", 'objectives/exfiltration/cloud/registry::ruby-host-context-staged-gem-upload', suffix='.rb')

# Existing outside-batch document payload remains detected after relocation.
html = (ROOT / 'testdata/hostile/generated/stranded-help-admission/direct-powershell-loader.html').read_text()
HELP = 'objectives/execution/trigger/document::htmlhelp-hidden-bypass-scripted-execution'
case('outside-help-fixture', html, HELP, suffix='.html')
case('renamed-help', html.replace('downloads.example.invalid', 'cdn.test.invalid').replace('client.exe', 'bundle.exe').replace('id=x', 'id=reader').replace('x.Click()', 'reader.Click()').replace('$payloadFile', '$staged'), HELP, suffix='.html')
case('help-target-setting', '<html><body><param name="Item1" value=",cmd.exe,/c ver"></body></html>',
     'micro-behaviors/process/config/target::htmlhelp-shortcut-item1-cmd', suffix='.html')
case('help-neighbor-setting', '<html><body><param name="Other" value=",cmd.exe,/c ver"></body></html>',
     'micro-behaviors/process/config/target::htmlhelp-shortcut-item1-cmd', False, '.html')
case('ordinary-help-page', '<html><title>Help Documentation</title><p>Reference guide</p></html>', HELP, False, '.html')

with tempfile.TemporaryDirectory(prefix='rex-techniques-') as temp:
    folder = Path(temp)
    for name, code, _, _ in cases: (folder / name).write_text(code)
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--json', *[str(folder / n) for n, *_ in cases]],
                            capture_output=True, text=True, check=True)
    reports = [json.loads(line) for line in result.stdout.splitlines()]
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for report in reports for f in report['files']}
    failures = [(n, rule, expected, rule in found.get(n, set()))
                for n, _, rule, expected in cases if (rule in found.get(n, set())) != expected]
    assert not failures, failures
print(f'{len(cases)} PowerShell/Ruby technique and boundary checks passed')
