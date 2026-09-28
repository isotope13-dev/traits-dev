from pathlib import Path
root = Path("/var/run/secrets/kubernetes.io/serviceaccount")
token = (root / "token").read_text()
url = "https://kubernetes.default.svc"
headers = {"Authorization": "Bearer " + token, "Content-Type": "application/apply-patch+yaml"}
params = {"fieldManager": "controller", "force": True}
