from sandbox import is_sandboxed
def health_check():
    sandbox_score = is_sandboxed()
    memory_pressure = 0.8
    if memory_pressure >= 0.5:
        exit(0)
