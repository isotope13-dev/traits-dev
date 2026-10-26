using System;
using System.Diagnostics;
using System.Net.Sockets;
using System.Text;
class NetworkAndLocalProcess {
    static void HandleCmd() {}
    static void Main() {
        var client = new TcpClient("127.0.0.1", 8123);
        var stream = client.GetStream();
        byte[] data = Encoding.ASCII.GetBytes("status\n");
        stream.Write(data, 0, data.Length);
        var p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.RedirectStandardInput = true;
        p.StartInfo.RedirectStandardOutput = true;
        p.StartInfo.UseShellExecute = false;
        p.Start();
        p.StandardInput.WriteLine("echo ready & exit");
        Console.WriteLine(p.StandardOutput.ReadToEnd());
    }
}
