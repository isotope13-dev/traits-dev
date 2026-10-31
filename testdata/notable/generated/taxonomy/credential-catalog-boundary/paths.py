from pathlib import Path
home = Path.home() / '.ssh'
stores = ['.npmrc', '.pypirc', '.netrc', '.git-credentials', '.vault-token', 'id_rsa', 'id_ed25519']
