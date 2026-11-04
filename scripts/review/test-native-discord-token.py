#!/usr/bin/env python3
"""Check native Discord token recovery and encrypted upload evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
recovery = r'''void f() {
char *db = "\\Local Storage\\leveldb"; char *prefix = "dQw4w9WgXcQ:";
master_key = decryptDPAPI(encryptedKey); Tokkos.push_back(decryptedToken);
}
'''
upload = r'''void g() {
string url = "/index.php?type=tknsprc&security=2";
string TKNdata = hwid + "|" + Tokenno;
string TKNdataEncrypted = Encrypt(TKNdata, enckey);
wrap::HttpsRequest(wrap::Url{url}, wrap::Body{ TKNdataEncrypted });
}
'''
cases = {'recovery.cpp': recovery, 'no-prefix.cpp': recovery.replace('dQw4w9WgXcQ:', 'ordinary:'),
         'no-decrypt.cpp': recovery.replace('decryptDPAPI', 'ordinaryDecode'),
         'upload.cpp': upload, 'no-body.cpp': upload.replace('TKNdataEncrypted }', 'other }'),
         'no-endpoint.cpp': upload.replace('tknsprc', 'other'),
         'no-https.cpp': upload.replace('HttpsRequest', 'formatRequest'),
         'exe-label.c': 'int EXE_INFEC;\n', 'exe-longer-name.c': 'int ExeInfection;\n'}
with tempfile.TemporaryDirectory(prefix='native-discord-token-') as temp:
    root = Path(temp)
    for name, source in cases.items():
        (root / name).write_text(source)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / name) for name in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    recover_id = 'objectives/credential-access/discord/leveldb::native-discord-leveldb-token-recovery'
    upload_id = 'objectives/exfiltration/stealer/credential::native-encrypted-token-post'
    assert recover_id in found['recovery.cpp']
    assert all(recover_id not in found[n] for n in ('no-prefix.cpp', 'no-decrypt.cpp'))
    assert upload_id in found['upload.cpp']
    assert all(upload_id not in found[n] for n in ('no-body.cpp', 'no-endpoint.cpp', 'no-https.cpp'))
    label = 'metadata/lang/source/naming/label::exe-page-or-infection-label'
    for name, expected in [('exe-label.c', 'MATCHED'), ('exe-longer-name.c', 'NOT MATCHED')]:
        trace = subprocess.run([args.cleave, '--traits-dir', str(repo), 'test-rules',
                                str(root / name), '--rules', label],
                               check=True, capture_output=True, text=True).stdout
        assert f'{expected} {label}' in trace, (name, trace)
    print('Discord token recovery and upload require distinct evidence.')
