<%@ page import="java.net.*,javax.crypto.*" %>
<%!
void helper() throws Exception {
  URL u = new URL("http://127.0.0.1/status");
  HttpURLConnection h = (HttpURLConnection) u.openConnection();
  Cipher c = Cipher.getInstance("AES/CFB/NoPadding");
  c.doFinal(new byte[0]);
}
%>
