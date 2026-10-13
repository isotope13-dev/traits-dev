# Heartbeat endpoint-path placement fixtures

Both files carry the same `/api/heartbeat` endpoint-path string in different
roles:

- `client.py` builds a client request URL from it (the MediaManager5
  `wallpaper.py` shape: `request("POST", f"{SERVER_URL}/api/heartbeat", …)`).
- `server.py` defines a server route handling it.

The matcher cannot distinguish the two, so the trait is a URL fact at
`micro-behaviors/communications/http/url/api-path::http-api-heartbeat-path`,
not server-side handling under `server/route`.

`check.py` asserts the new ID fires as notable on both files and the old
`server/route::python-heartbeat-route` ID is absent.
