def grep_search(pattern, state):
    files = state.get("files", {})
    return pattern in files and regex.search(pattern)
