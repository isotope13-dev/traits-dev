"""Scan capability-placement controls without executing their contents."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CONTROLS = [
    ("input_device.py", '# virtualbox mouse uses a VirtualBox USB tablet\nDEVICE = "/dev/input/by-id/usb-VirtualBox_USB_Tablet-event-mouse"\n',
     ["micro-behaviors/os/virtualization/hypervisor::python-virtualbox-word-reference"], []),
    ("secret_client.py", '''import os
import requests
token = os.getenv("KAGGLE_USER_SECRETS_TOKEN")
response = requests.post("https://www.kaggle.com/requests/GetUserSecretByLabelRequest",
    headers={"X-Kaggle-Authorization": f"Bearer {token}"}, json={"Label": "api-key"})
value = response.json()["result"]["secret"]
''', ["micro-behaviors/os/env/secret-name::platform-secret-store-session-token-name",
      "micro-behaviors/communications/rpc::named-secret-read-rpc-reference",
      "micro-behaviors/communications/rpc::secret-read-rpc-session-token-context"], []),
    ("remote_notebook.py", '''from google.colab import output
from IPython.display import Javascript, display
display(Javascript("async function identify() { return import('https://cdn.example.net/fingerprint.js'); }"))
visitor = output.eval_js("identify()")
''', ["micro-behaviors/os/module/require::python-remote-es-module-import",
      "micro-behaviors/process/interpreter/eval/indirect::notebook-js-result-readback",
      "micro-behaviors/process/interpreter/eval/indirect::notebook-remote-js-result-roundtrip"],
     ["micro-behaviors/os/module/require::python-remote-es-module-import"]),
    ("local_notebook.py", '''from google.colab import output
from IPython.display import Javascript, display
display(Javascript("async function identify() { return import('./local.js'); }"))
value = output.eval_js("identify()")
''', ["micro-behaviors/process/interpreter/eval/indirect::notebook-js-result-readback"], []),
    ("browser.js", 'async function identify() { return FingerprintJS.load(); }\n',
     ["micro-behaviors/os/sysinfo/hardware::fingerprintjs-load-call"], []),
    ("predicate.py", 'def is_hosted_notebook():\n    return False\n',
     ["micro-behaviors/data/source/function/names::hosted-notebook-predicate-name"], []),
]

with tempfile.TemporaryDirectory(prefix="wheel-placement-controls-") as scratch:
    for name, source, required, expected_suspicious in CONTROLS:
        path = Path(scratch) / name
        path.write_text(source)
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "json", str(path)],
            capture_output=True, text=True, check=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1", "CLEAVE_NO_UPDATE_CHECK": "1"},
        )
        traits = json.loads(result.stdout)["files"][0]["traits"]
        ids = {t["id"] for t in traits}
        assert set(required) <= ids, (name, "missing", set(required) - ids)
        assert not [t for t in traits if t["crit"] == 5], (name, "hostile findings", traits)
        suspicious = {t["id"] for t in traits if t["crit"] == 4}
        assert suspicious == set(expected_suspicious), (name, "suspicious", suspicious)
        old_prefixes = (
            "objectives/discovery/system/fingerprint/notebook::",
            "objectives/credential-access/credential-manager/store-api::platform-secrets-",
        )
        assert not any(i.startswith(old_prefixes) for i in ids), (name, "old capability location")
        print(name, "passed", flush=True)
print("6 wheel capability-placement controls passed")
