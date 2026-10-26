"""Static-only fixture: imports plus synthetic in-memory records."""
import ctypes
import json
import shutil
import sqlite3
import tempfile

from cryptography.hazmat.primitives.ciphers import Cipher


def inspect_synthetic_record():
    # The database exists only in memory and contains no credentials.
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE fixture (value TEXT)")
    db.execute("INSERT INTO fixture VALUES (?)", (json.dumps({"value": "dummy"}),))
    return db.execute("SELECT value FROM fixture").fetchone()
