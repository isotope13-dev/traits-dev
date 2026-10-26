Set shell = CreateObject("WScript.Shell")
command = "cmd.exe /c powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -NonInteractive -Command " & WScript.Arguments(0)
shell.Run command, 0, False
