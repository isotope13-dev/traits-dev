"""Exercise the original fixture against recording objects; no SSH or socket."""
from pathlib import Path
import runpy

events = []


class RecordingChannel:
    def get_pty(self, **kwargs):
        events.append(("get_pty", kwargs))

    def invoke_shell(self):
        events.append(("invoke_shell",))

    def sendall(self, data):
        events.append(("sendall", data))


class RecordingTransport:
    def auth_password(self, *args, **kwargs):
        events.append(("auth_password", args, kwargs))

    def open_session(self, **kwargs):
        events.append(("open_session", kwargs))
        return RecordingChannel()


namespace = runpy.run_path(str(Path(__file__).with_name("policy-fixture.py")))
assert not events
namespace["install_router_admin"](RecordingTransport(), "lab", "audit", 17)
assert events[0] == ("auth_password", ("-7", "lab"), {"fallback": False})
assert events[-2] == ("sendall", b"audit\x0017\x00\x04\x04")
assert events[-1][1].endswith(b'group=full\r')
for event in events:
    print(repr(event))
