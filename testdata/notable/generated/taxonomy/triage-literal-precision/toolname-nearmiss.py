def send_event(tool_name, tool_args):
    print(f"[TOOL_START] Invoking: {tool_name}")
    post("/api/telemetry/tool-call", {"tool": tool_name, "args": tool_args})
