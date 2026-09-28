from pathlib import Path
root = Path("/tmp/parser")
value = (root / "token").read_text()
