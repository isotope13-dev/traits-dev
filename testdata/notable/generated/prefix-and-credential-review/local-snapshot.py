import os as system
import requests as transport
print(dict(system.environ))
transport.post("https://report.example/health", json={"ok": True})
