<%@ page import="java.sql.*" %>
<% DatabaseMetaData md=conn.getMetaData();
ResultSet tables=md.getTables(null, null, "%", null);
ResultSet definition=stmt.executeQuery("SHOW CREATE TABLE " + table); %>
