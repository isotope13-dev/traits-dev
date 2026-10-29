import time

data = []
def failback():
    while True:
        str = "X" * 1024 * 1024
        data.append(str)
        time.sleep(0.1)
