from pathlib import Path
settings_path = Path("myapp/settings.json")
hooks = {"hooks": {"Stop": []}}
settings_path.write_text(str(hooks))
