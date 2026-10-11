<%
Set shell = Server.CreateObject("WScript.Shell")
shell.Run "cmd.exe /c ver", 0, True
%>
