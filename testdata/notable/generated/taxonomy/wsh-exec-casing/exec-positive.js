var shell = WScript.CreateObject("WScript.Shell");
var proc = shell.Exec("cmd /c whoami");
while (!proc.StdOut.AtEndOfStream) { WScript.Echo(proc.StdOut.ReadLine()); }
