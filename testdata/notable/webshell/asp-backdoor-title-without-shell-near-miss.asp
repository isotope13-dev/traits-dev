<html>
<title>Backdoor detection notes</title>
<body>
<%
Dim q
q = Request.QueryString("page")
Response.Write "Reading " & Server.HTMLEncode(q)
%>
</body>
</html>
