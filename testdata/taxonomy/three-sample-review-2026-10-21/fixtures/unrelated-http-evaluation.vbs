Set req = CreateObject("MSXML2.XMLHTTP")
req.open "GET", "https://example.org/news", False
req.send
WScript.Echo req.responseText
localCode = "Function add(a,b): add=a+b: End Function"
ExecuteGlobal localCode
