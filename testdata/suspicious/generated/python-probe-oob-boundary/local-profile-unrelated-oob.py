# authorized-pentest probe example
import socket, json, urllib.request
# An unrelated external documentation link:
documentation_url = "https://webhook.site/11111111-1111-1111-1111-111111111111"
def send_local_profile():
    try:
        info = {"host": socket.gethostname()}
        req = urllib.request.Request("http://localhost:8080/status", data=json.dumps(info).encode(),
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=15).read()
    except Exception:
        pass
send_local_profile()
