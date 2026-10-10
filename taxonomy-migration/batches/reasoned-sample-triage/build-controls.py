"""Build inert positive/near-miss inputs for this triage batch."""
from pathlib import Path
import sys, zipfile

fixtures = Path(__file__).parent / 'fixtures'
with zipfile.ZipFile(sys.argv[1], 'w') as archive:
    for path in sorted(fixtures.iterdir()):
        archive.write(path, path.name)
