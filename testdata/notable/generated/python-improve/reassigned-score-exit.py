from sandbox import is_sandboxed
def health_check():
    score = is_sandboxed()
    score = read_memory_pressure()
    if score >= 0.5:
        exit(0)
