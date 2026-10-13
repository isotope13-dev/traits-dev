from pathlib import Path
import json
settings_path = Path.home() / ".claude" / "settings.json"
hooks = {"hooks": {"Stop": []}}
settings_path.write_text(json.dumps(hooks))
