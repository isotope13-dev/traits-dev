Local $r = DllCall("kernel32.dll", "bool", "CreateProcessW", "wstr", "child.exe", "wstr", "", "ptr", 0, "ptr", 0, "int", 0, "dword", 4, "ptr", 0)
Local $r = DllCall("kernel32.dll", "ptr", "VirtualAllocEx", "handle", $h, "ptr", 0, "dword_ptr", 4096, "dword", 4096, "dword", 64)
Local $r = DllCall("kernel32.dll", "bool", "WriteProcessMemory", "handle", $h, "ptr", $p, "ptr", $buf)
Local $r = DllCall("kernel32.dll", "bool", "ReadProcessMemory", "ptr", $h, "ptr", $p, "ptr", $buf)
