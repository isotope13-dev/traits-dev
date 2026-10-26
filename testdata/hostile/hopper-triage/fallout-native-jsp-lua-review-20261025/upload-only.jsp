<%@ page import="java.io.*" %>
<% byte[] data=request.getInputStream().readAllBytes(); new FileOutputStream("upload.dat").write(data); %>