import os
from zipfile import ZipFile
key = os.path.expanduser('~/.ssh/id_rsa')
with ZipFile('/tmp/keys.zip', 'w') as archive:
    archive.write(key)
