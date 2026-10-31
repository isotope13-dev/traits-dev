import os
products = ["Schneider Electric Unity", "Program Files Siemens WinCC"]
for path in products:
    print(os.path.exists(path))
