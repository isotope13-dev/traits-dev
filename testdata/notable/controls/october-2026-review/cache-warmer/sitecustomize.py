import os, time
def detach():
    if os.fork() > 0:
        return False
    os.setsid()
    return True
def warm():
    while True:
        for root, _dirs, files in os.walk("/tmp/cache"):
            for name in files:
                try:
                    os.stat(os.path.join(root, name))
                except OSError:
                    pass
        time.sleep(600)
if detach():
    warm()
