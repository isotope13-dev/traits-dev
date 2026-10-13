from pathlib import Path
settings = Path(".claude/settings.json")
settings.write_text("{}")
