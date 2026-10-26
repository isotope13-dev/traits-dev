<%@ page import="java.io.*" %>
<% String value=request.getParameter("cmd"); out.println(value); Runtime.getRuntime().exec("cmd /c echo fixed"); %>
