import os
for name in os.listdir("/storage/emulated/0"):
    if name.startswith("."):
        continue
