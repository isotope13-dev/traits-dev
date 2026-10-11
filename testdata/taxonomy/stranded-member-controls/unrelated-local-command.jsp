<%@ page import="java.io.*" %>
<% out.println(request.getParameter("cmd")); String cmd="echo fixed"; Process p=Runtime.getRuntime().exec(cmd); %>
