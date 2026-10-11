<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
out.println(cmd);
Process p = Runtime.getRuntime().exec("/usr/bin/date");
out.println(p.getInputStream().read());
%>
