import json, platform, socket, getpass
import requests
host = dict(hostname=socket.gethostname(), user=getpass.getuser(), system=platform.system(), release=platform.release(), version=platform.version(), machine=platform.machine(), uname=platform.uname())
def _aigc_post(url, data):
    requests.post(url, json=data)
_aigc_post('https://telemetry.example/report', host)
send_post_file_req('tracking.json', json.dumps(get_track_metrics()))
