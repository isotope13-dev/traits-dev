from pathlib import Path
import httpx
payload=Path.home().joinpath(".git-credentials").read_text()
payload="healthy"
httpx.post("https://service.invalid/health", content=payload)
