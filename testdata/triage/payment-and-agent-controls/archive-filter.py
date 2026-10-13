import os, zipfile
with zipfile.ZipFile("dataset.zip", "w") as z:
    for name in os.listdir("/storage/emulated/0"):
        if name.startswith("."):
            continue
        z.write(name)
