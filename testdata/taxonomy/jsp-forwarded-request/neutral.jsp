<%@page import="java.io.*"%><%
String cmd=request.getParameter("cmd");
Process p=Runtime.getRuntime().exec("id");
new FileOutputStream("fixed.txt").write("fixed".getBytes());
out.print(cmd);
%>