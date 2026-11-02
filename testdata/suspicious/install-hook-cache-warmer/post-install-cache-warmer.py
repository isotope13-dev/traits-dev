"""Build helpers run after installation."""

import threading
import time


def post_install_build():
    """
    Post-install hook - warms the local model cache after setup.py finishes.
    """
    def warm_cache():
        time.sleep(2)

    worker = threading.Thread(target=warm_cache, daemon=False)
    worker.start()
    time.sleep(1)
