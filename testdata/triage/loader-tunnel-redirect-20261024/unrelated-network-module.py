import urllib.request
image = urllib.request.urlopen("https://example.org/image.png").read()
# A local plugin runs independently of the image response.
source = "import importlib.util; spec = importlib.util.spec_from_file_location('local', 'plugin.py'); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)"
filename = "cache.py"
with open("image.bin", "wb") as f:
    f.write(image)
