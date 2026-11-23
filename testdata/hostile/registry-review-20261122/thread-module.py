import importlib.util
import threading
spec = importlib.util.spec_from_file_location('worker', '/tmp/hidden.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
threading.Thread(target=module.main, daemon=True).start()
