#!/usr/bin/env python3
"""Check neutral survey severity, source calls, and HTTP type anchors."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[3]
engine = os.environ.get('CLEAVE', 'cleave')
get_text = 'micro-behaviors/communications/http/get::getstringasync'
get_bytes = 'micro-behaviors/communications/http/get::getbytearrayasync'
survey = 'objectives/discovery/cloud/directory::entra-directory-enumeration'
cross = 'objectives/discovery/cloud/directory::cross-saas-user-directory-recon'
tracked = {get_text, get_bytes, survey, cross}

def source(body):
    return 'using System.Net.Http; class C { static async void M() { ' + body + ' } }'

paths = ('string[] paths = {"/beta/tenantRelationships/getResourceTenants", '
         '"/beta/users/{u}/roleManagement/directory/transitiveRoleAssignments", '
         '"/beta/users/{u}/ownedObjects/Microsoft.graph.ServicePrincipal"}; '
         'string host = "https://graph.microsoft.com"; ')
cases = [
    ('text-get', source('using var c = new HttpClient(); await c.GetStringAsync("https://example.org");'), {get_text}),
    ('bytes-get', source('using var c = new HttpClient(); await c.GetByteArrayAsync("https://example.org");'), {get_bytes}),
    ('both-get', source('using var c = new HttpClient(); await c.GetStringAsync("https://example.org"); await c.GetByteArrayAsync("https://example.org");'), {get_text, get_bytes}),
    ('cache-only', source('await cache.GetStringAsync("key"); await cache.GetByteArrayAsync("key");'), set()),
    ('method-comments', source('using var c = new HttpClient(); /* await c.GetStringAsync("x"); await c.GetByteArrayAsync("x"); */'), set()),
    ('method-string', source('using var c = new HttpClient(); string s = "GetStringAsync GetByteArrayAsync";'), set()),
    ('graph-survey', source(paths), {survey}),
    ('cross-saas-survey', source(paths + 'string export = "/sys_user_list.do?CSV";'), {survey, cross}),
    ('single-resource', source('string host = "https://graph.microsoft.com"; string path = "/beta/tenantRelationships/getResourceTenants";'), set()),
    ('survey-comments', source('/* ' + paths + ' */'), set()),
]

with tempfile.TemporaryDirectory(prefix='directory-http-controls-', dir=repo) as temporary:
    def run(case):
        name, content, expected = case
        path = Path(temporary, name + '.cs')
        path.write_text(content)
        proc = subprocess.run([engine, '--traits-dir', str(repo), str(path), '--format', 'json'], capture_output=True, text=True)
        assert proc.returncode == 0, (name, proc.stderr)
        report = json.loads(proc.stdout)
        traits = [t for f in report['files'] for t in f.get('traits', [])]
        observed = {t['id'] for t in traits}
        assert observed & tracked == expected, (name, observed & tracked, expected)
        assert not [t for t in traits if t['crit'] >= 4], (name, traits)
        for t in traits:
            if t['id'] in expected:
                assert t['crit'] == 3, (name, t)
        return name + ': PASS'
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(run, cases):
            print(result, flush=True)
