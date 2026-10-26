using System.Net;
using System.IO;
using System.Diagnostics;
class Probe {
 static void Main() {
  var server = new HttpListener();
  server.Prefixes.Add("http://localhost:9090/");
  server.Start();
  var request = server.GetContext();
  request.Response.StatusCode = 401;
  request.Response.AddHeader("WWW-Authenticate", "NTLM " + token);
 }
}
