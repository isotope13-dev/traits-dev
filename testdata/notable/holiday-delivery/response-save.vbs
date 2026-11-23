Set request = CreateObject("Microsoft.XMLHTTP")
Set output = CreateObject("ADODB.Stream")
request.open "GET", "https://example.org/report.csv", False
request.send
output.open
output.write request.responseBody
output.savetofile "report.csv", 2
