def handle_hook(payload):
    tool_name = payload.get("tool_name", "unknown")
    log("dispatching " + tool_name)
    return route(tool_name)
