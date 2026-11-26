// Logon script: sets the corporate home page.
var sh = new ActiveXObject("WScript.Shell");
var key = "HKCU\\Software\\Microsoft\\Internet Explorer" + "\\Main\\Start Page";
sh.RegWrite(key, "http://intranet.example.com/");
