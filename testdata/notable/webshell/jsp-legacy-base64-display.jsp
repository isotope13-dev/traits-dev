<%@page import="java.util.*"%><% byte[] data = new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()); out.print(data.length); %>
