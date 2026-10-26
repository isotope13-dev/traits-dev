"""Import-only control; no browser data, decrypt call, or credential access."""
import ctypes
import json
import shutil
import sqlite3
import tempfile

from cryptography.hazmat.primitives.ciphers import Cipher
