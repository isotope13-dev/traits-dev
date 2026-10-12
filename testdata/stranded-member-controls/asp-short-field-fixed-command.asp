<%
Set runner = Server.CreateObject("WScript.Shell")
color = Request.Form("C")
Call runner.Run("cmd.exe /c ver", 0, True)
Response.Write color
Call runner.Run("cmd.exe /c del C:\temp\output.txt", 0, True)
%>
