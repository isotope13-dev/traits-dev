"""Static-only fixture: synthetic local data, never connects or exports."""
import json
import requests
import shutil
import subprocess
import tempfile
import threading
import websocket
import zipfile

# A fictional path string for matcher coverage; no file is opened or created.
SYNTHETIC_PROFILE = "/tmp/fictional-profile/Cookies"
WebSocket = websocket.WebSocket


def make_local_fixture_record():
    return json.dumps({"session": "not-a-credential", "profile": "fixture"})


def construct_unconnected_client():
    # The constructor is only a static marker; this function is never called.
    return websocket.WebSocket()
