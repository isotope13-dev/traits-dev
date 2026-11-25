# Diagnostics routes exposed by a loopback-only local daemon.
ROUTES = {
    "GET": ["/api/debug/memory", "/api/debug/event-loop", "/api/debug/mesh"],
    "POST": ["/api/debug/client-trace", "/api/debug/cpu-profile"],
}


def list_routes(method):
    return ROUTES.get(method, [])
