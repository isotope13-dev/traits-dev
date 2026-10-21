import json
def merge(mcp_config, existing_tools):
    for tool in mcp_config["allowedTools"]:
        if tool.startswith("mcp__"):
            existing_tools.add(tool)
    return existing_tools
