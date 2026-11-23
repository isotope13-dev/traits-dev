import importlib.util
import os
import threading


def load_plugin(path):
    spec = importlib.util.spec_from_file_location(
        "plugin", os.path.join(os.path.dirname(__file__), path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _refresh_cache():
    print("cache refreshed")


threading.Thread(target=_refresh_cache, daemon=True).start()


def main():
    print("Plugin host ready.")
