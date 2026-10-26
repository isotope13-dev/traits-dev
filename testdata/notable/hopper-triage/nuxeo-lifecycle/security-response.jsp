<%@ page import="java.util.UUID" %>
<%
String nonce = UUID.randomUUID().toString();
response.setHeader("Content-Security-Policy", "script-src 'nonce-" + nonce + "'");
%>
