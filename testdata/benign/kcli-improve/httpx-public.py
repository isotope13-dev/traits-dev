from pathlib import Path
import httpx
secret=Path.home().joinpath(".git-credentials").read_text()
public=Path("/tmp/status.txt").read_text()
httpx.post("https://service.invalid/health", content=public)
