// Mail account inventory for the help desk: lists the display names only.
var sh = new ActiveXObject("WScript.Shell");
var base = "HKCU\\Software\\Microsoft\\Internet Account Manager\\Accounts\\00000001\\";
var name = sh.RegRead(base + "Account Name");
WScript.Echo("Account: " + name);
