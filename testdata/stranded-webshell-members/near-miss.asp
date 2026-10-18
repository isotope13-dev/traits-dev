<%
Set fs = Server.CreateObject("Scripting.FileSystemObject")
Set stream = fs.OpenTextFile("manual.txt", 2, False, 0)
stream.Write "updated"
%>
