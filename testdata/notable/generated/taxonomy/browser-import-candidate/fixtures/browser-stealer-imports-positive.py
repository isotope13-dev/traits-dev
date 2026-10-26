"""Static-only fixture: synthetic in-memory row and throwaway archive name."""
import aiohttp
import base64
import ctypes
import json
import requests
import shutil
import sqlite3
import subprocess
import tempfile
import zipfile

from cryptography.hazmat.primitives.ciphers import Cipher


def synthetic_row():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE fixture (value TEXT)")
    db.execute("INSERT INTO fixture VALUES (?)", (base64.b64encode(b"dummy"),))
    return db.execute("SELECT value FROM fixture").fetchone()
