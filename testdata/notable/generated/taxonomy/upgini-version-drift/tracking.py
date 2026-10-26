from json import dumps


def submit(client):
    files = {"tracking": ("tracking.json", dumps(get_track_metrics()).encode(), "application/json")}
    return client._send_post_file_req_v2("/search", files)
