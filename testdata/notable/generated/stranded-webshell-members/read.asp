<%
Set fs = Server.CreateObject("Scripting.FileSystemObject")
Set stream = fs.OpenTextFile("manual.txt", 1, False, 0)
Response.Write stream.ReadAll
Set network = Server.CreateObject("WScript.Network")
Response.Write network.ComputerName
%>
