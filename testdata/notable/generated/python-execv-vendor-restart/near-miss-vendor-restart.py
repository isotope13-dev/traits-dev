# Benign near-miss for python-tunnel-body-execv-relaunch: the same fetch and
# os.execv restart, but the code source is the project's own vendor domain,
# not an ephemeral tunnel. The hostile composite must not fire without the
# tunnel-host leg; only the notable atoms (execv, response body read) should.
import os
import sys
import requests

UPDATE_URL = "https://updates.example-tool.dev/download/tool-latest.py"
script_path = __file__

response = requests.get(UPDATE_URL, timeout=10)

with open(script_path, 'w') as script_file:
    script_file.write(response.text)

os.execv(sys.executable, [sys.executable] + sys.argv)
