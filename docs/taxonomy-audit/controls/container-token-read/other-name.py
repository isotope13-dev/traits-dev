from pathlib import Path
root = Path("/tmp/parser")
value = (root / "namespace").read_text()
