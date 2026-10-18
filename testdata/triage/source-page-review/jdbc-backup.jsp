<%@ page import="java.sql.*" %>
<% String table=request.getParameter("table");
Class.forName(driver);
Connection conn=DriverManager.getConnection(url,username,password);
BufferedWriter writer=new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path+".txt")));
ResultSet rs=conn.createStatement().executeQuery("SELECT * FROM "+table);
while(rs.next()) { writer.append("INSERT INTO "+table+" VALUES('");writer.append(rs.getString(1));writer.append("');"); }
writer.close(); %>
