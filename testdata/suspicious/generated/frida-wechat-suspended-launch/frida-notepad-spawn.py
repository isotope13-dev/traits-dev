import ctypes, frida
k = ctypes.windll.kernel32
si = ctypes.create_string_buffer(104)
pi = ctypes.create_string_buffer(24)
k.CreateProcessW(None, "C:\\Program Files\\Tencent\\WeChat\\Notepad.exe", None, None, False, 4, None, None, si, pi)
pid = int.from_bytes(pi.raw[16:20], "little")
session = frida.attach(pid)
session.create_script("send(1)").load()
k.ResumeThread(int.from_bytes(pi.raw[8:16], "little"))
