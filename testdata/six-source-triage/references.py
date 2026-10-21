import builtins
exec_ = getattr(builtins, "exec")
print_ = getattr(builtins, "print", None)
module_names = ["http.server", "SimpleHTTPServer", "BaseHTTPServer"]
handler_name = "HTTPBasicAuthHandler"
verbs = ["print", "token"]
class _SixMetaPathImporter:
    pass
