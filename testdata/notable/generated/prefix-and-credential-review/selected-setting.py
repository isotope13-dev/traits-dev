import os as system
import requests as transport

transport.post("https://rotated.invalid/telemetry", json=dict(status=system.environ.get("TERM")))
