import glob
from pathlib import Path
for entry in glob.glob('/proc/*/environ')[:300]:
    try:
        content = Path(entry).read_bytes().decode(errors='replace')
    except OSError:
        pass
