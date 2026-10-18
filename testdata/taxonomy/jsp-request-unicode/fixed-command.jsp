<%@page import="java.io.*"%>
<%
String ignored=request.getParameter("cmd");Process p=Runtime.getRuntime().exec("cmd.exe /c ver");
%>
