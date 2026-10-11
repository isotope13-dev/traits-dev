<%@ page import="java.io.*" %>
<%
String cmd = request.getParameter("cmd");
out.println(cmd);
String local = "/usr/bin/date";
Process p = Runtime.getRuntime().exec(local);
out.println(p.getInputStream().read());
%>
