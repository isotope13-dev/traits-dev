import os, subprocess, sys, urllib.request
image = urllib.request.urlopen("https://example.org/picture.png").read()
with open("picture.png", "wb") as out:
    out.write(image)
SOURCE = "import importlib.util; spec = importlib.util.spec_from_file_location('local', sys.argv[1]); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)"
def start():
    boot = os.path.join("cache", "local.py")
    with open(boot, "w", encoding="utf-8") as out:
        out.write(SOURCE)
    child = subprocess.Popen([sys.executable, boot, "local-plugin.py"])
    return child.wait()
