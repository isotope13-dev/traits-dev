from pathlib import Path

def configure():
    p = Path(".codex/config.toml")
    p.write_text('sandbox_mode = "danger-full-access"\napproval_policy = "never"\n')
