// Boundary: FileSystemObject plus a self-path reference but no copy call
// of any form must not read as a self-copy.
var fso = WScript.CreateObject("Scripting.FileSystemObject");
var me = WScript.ScriptFullName;
WScript.Echo("running from " + me);
