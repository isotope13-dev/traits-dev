from pathlib import Path

def update_index():
    Path("ai_docs/INDEX.md").write_text("index")






























def inspect_settings():
    return Path(".claude/settings.json").read_text()
