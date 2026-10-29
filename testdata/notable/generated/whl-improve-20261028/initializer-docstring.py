import os
import threading

def collect():
    blob.upload_from_string(os.getenv("RUN", ""))

"""
class Worker:
    threading.Thread(target=collect()).start()
"""
