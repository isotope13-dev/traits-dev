"""Local-only control: fake record serialization without network imports."""
import json
import sqlite3
import tempfile

SYNTHETIC_PROFILE = "/tmp/fictional-profile/Cookies"


def local_record():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE fixture (value TEXT)")
    db.execute("INSERT INTO fixture VALUES (?)", (json.dumps({"value": "dummy"}),))
    return db.execute("SELECT value FROM fixture").fetchone()
