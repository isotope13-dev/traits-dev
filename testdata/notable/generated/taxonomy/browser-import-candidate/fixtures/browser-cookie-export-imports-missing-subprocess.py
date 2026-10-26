"""Near miss: required imports and fake path, but no subprocess import."""
import json
import requests
import shutil
import tempfile
import threading
import websocket
import zipfile

SYNTHETIC_PROFILE = "/tmp/fictional-profile/Cookies"
