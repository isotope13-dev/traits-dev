<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
cmd = "/usr/bin/date";
Process p = Runtime.getRuntime().exec(cmd);
out.println(p.getInputStream().read());
%>
