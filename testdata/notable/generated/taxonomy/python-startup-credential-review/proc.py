from pathlib import Path

def inventory():
    return list(Path('/proc').glob('[0-9]*/environ'))
