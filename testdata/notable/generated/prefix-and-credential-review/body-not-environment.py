import os as system
import requests as transport
transport.post("https://report.example/health", json=dict({"ok": True}))
