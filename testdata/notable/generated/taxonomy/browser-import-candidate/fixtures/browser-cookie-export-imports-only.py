"""Import-only control; no WebSocket call, local file access, or network use."""
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


def construct_unconnected_client():
    # Static API reference only; this function is never called.
    return websocket.WebSocket()
