var shell = WScript.CreateObject("WScript.Shell");
var fs = WScript.CreateObject("Scripting.FileSystemObject");
var self = WScript.ScriptFullName;
var host = WScript.FullName.replace(/wscript/i,"cscript").replace(/syswow64/i,"system32");
shell.Run('"'+host+'" //nologo //E:JScript "'+self+'"',0,false);
var proc = shell.Exec("powershell.exe -WindowStyle Hidden -Command -");
proc.StdIn.Write("Write-Output 'done'");
proc.StdIn.Close();
fs.DeleteFile("C:/cache/old.log",true);
