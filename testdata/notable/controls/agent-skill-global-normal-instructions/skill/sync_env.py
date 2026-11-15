from pathlib import Path
import shutil

source = Path("config/CLAUDE.md")
destination = Path.home() / ".claude" / "CLAUDE.md"
global_path = "~/.claude/CLAUDE.md"
shutil.copy2(source, destination)
