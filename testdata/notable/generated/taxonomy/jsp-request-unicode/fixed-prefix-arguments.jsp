<%@page import="java.io.*"%>
<%
Process p=Runtime.getRuntime().exec("/bin/echo " + request.getParameter("cmd"));out.println(p.getInputStream());
%>
