<%
body=Request.BinaryRead(Request.TotalBytes)
Response.BinaryWrite body
%>
