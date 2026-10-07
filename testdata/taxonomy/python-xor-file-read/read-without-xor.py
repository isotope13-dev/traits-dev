from pathlib import Path


content = Path("payload.bin").read_bytes()
print(content.decode("utf-8", errors="ignore"))
