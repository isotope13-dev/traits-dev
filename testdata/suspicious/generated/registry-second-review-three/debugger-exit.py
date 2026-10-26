import ctypes, sys

def guard():
    if ctypes.windll.kernel32.IsDebuggerPresent():
        sys.exit(0)
