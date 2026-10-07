import os
from zipfile import ZipFile
state = os.path.expanduser('~/.cache/state.json')
with ZipFile('/tmp/cache.zip', 'w') as archive:
    archive.write(state)
