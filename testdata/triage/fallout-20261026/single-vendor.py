from pathlib import Path
data = (Path.home() / '.codex/auth.json').read_bytes()
