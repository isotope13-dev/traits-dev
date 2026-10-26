import ctypes

def diagnostic():
    print(ctypes.windll.kernel32.IsDebuggerPresent())
