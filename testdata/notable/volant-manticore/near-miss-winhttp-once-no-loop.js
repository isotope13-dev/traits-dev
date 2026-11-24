var http = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
http.Open("GET", "https://example.org/version.txt", false);
http.Send();
var sh = new ActiveXObject("WScript.Shell");
sh.Run("notepad.exe", 1, false);
