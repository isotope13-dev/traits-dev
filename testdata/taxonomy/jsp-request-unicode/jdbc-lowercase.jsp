<%@page import="java.sql.*"%>
<% Statement m=c.createStatement(); ResultSet r=m.executeQuery("select * from inventory"); %>
