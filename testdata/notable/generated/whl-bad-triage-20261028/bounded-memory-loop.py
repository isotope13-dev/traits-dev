import time
def warm_cache():
    data = []
    while True:
        block = "X" * 1024 * 1024
        data.append(block)
        if len(data) >= 4:
            break
        time.sleep(0.1)
    return data
