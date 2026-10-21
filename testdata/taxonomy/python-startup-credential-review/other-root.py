from pathlib import Path

def inventory():
    return list(Path('/archive').glob('[0-9]*/environ'))
