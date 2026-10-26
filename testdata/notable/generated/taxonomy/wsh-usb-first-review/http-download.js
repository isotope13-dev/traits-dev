var req = WScript.CreateObject("MSXML2.XMLHTTP");
req.open("GET", downloadUrl, false);
req.setRequestHeader("Cache-Control", "max-age=0");
req.send();
var stream = WScript.CreateObject("ADODB.Stream");
stream.Type = 1;
stream.Open();
stream.Write(req.responseBody);
stream.SaveToFile("download.bin");
