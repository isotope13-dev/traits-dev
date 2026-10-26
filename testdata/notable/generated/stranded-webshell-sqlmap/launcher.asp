<%
Set shell = Server.CreateObject("WScript.Shell")
shell.Run "win.com cmd.exe /c ver", 0, True
%>
