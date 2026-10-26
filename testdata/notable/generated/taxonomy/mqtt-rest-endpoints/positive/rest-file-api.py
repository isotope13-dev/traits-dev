"""Remote workspace file sync over the agent server HTTP API (no MQTT)."""


def upload(client, local_path, remote_path):
    with open(local_path, "rb") as f:
        return client.post("/file/upload", files={"file": f})


def download(client, remote_path, local_path):
    r = client.get("/file/download", params={"path": str(remote_path)})
    with open(local_path, "wb") as f:
        f.write(r.content)
