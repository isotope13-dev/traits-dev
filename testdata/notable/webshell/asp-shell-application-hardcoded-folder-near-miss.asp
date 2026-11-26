<%@ Language=VBScript %>
<html>
<title>Backup status page</title>
<body>
<%
Dim sh, fld, itm
set sh = Server.CreateObject("Shell.Application")
set fld = sh.NameSpace("D:\\backups")
for each itm in fld.Items
  Response.Write itm.Name & "<br>"
next
%>
</body>
</html>
