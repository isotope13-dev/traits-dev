import psutil
analysis_tools = ["wireshark", "x64dbg", "procmon", "ollydbg"]
for process in psutil.process_iter():
    if any(tool in process.name() for tool in analysis_tools):
        print(process.name())
