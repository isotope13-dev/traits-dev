import psutil
for process in psutil.process_iter():
    if process.info.get("name") in {"TIA Portal.exe", "WinCC.exe"}:
        continue
