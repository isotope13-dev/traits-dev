<%@ Page Language="C#" %>
<%
System.Diagnostics.Process p = new System.Diagnostics.Process();
p.StartInfo.Arguments="/c ver";
%>
