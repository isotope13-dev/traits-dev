var fso = new ActiveXObject("Scripting.FileSystemObject");
var source = WScript.ScriptFullName;
fso.CopyFile(source, "C:\\Users\\Public\\backup.js", true);
