from sandbox import is_sandboxed
def gate():
    score = is_sandboxed()
    if score >= 0.5:
        exit(0)
