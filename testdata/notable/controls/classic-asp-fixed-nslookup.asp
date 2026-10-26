<%
query = trim(Request.Form("query"))
query = replace(query, " ", "")
query = replace(query, ";", "")
command = "nslookup -type=ANY " & query
Set objWShell = Server.CreateObject("WScript.Shell")
Set objCmd = objWShell.Exec(command)
Response.Write objCmd.StdOut.Readall()
%>
