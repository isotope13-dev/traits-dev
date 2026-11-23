Set fs = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
p = fs.BuildPath(fs.GetSpecialFolder(2).Path, "maintenance.js")
Set output = fs.CreateTextFile(p, True)
output.Write "WScript.Echo 1"
output.Close
cmd = "wscript """ & p & """"
window = 0
shell.Run cmd, window, True
