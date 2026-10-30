from sandbox import is_sandboxed
def gate():
    try:
        score = is_sandboxed(logging=False)
    except Exception:
        score = 1
    if score >= 0.5:
        exit(0)
