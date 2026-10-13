import importlib.util
if importlib.util.find_spec("pdf") is None:
    print("missing")
