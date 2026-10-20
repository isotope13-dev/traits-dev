<%@ page import="java.io.*, java.net.*" %>
<%
Socket peer = new Socket(host, port);
Socket upstream = new Socket(otherHost, otherPort);
Object a = new CopyWorker(upstream.getInputStream(), peer.getOutputStream());
Object b = new CopyWorker(peer.getInputStream(), upstream.getOutputStream());
%>
