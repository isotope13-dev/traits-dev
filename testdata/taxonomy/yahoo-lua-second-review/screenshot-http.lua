-- Screen-sharing API declarations do not establish unauthorized upload.
local capture = {"GetSystemMetrics", "CreateDIBSection", "BitBlt"}
local client = {"InternetOpenUrlW", "HttpSendRequestW"}
local endpoint = "http://8.8.8.8/support"
local contentType = "multipart/form-data"
return capture, client, endpoint, contentType
