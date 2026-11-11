// Positive variant: renamed identifiers, switch-case-free same technique, different buffer method
using System;
using System.IO;
using System.Net.Sockets;
using System.Threading.Tasks;

public class PivotLoop
{
    public static async Task SpinAsync(string opsHost, int opsPort)
    {
        while (true)
        {
            var ctrl = new TcpClient();
            await ctrl.ConnectAsync(opsHost, opsPort);
            var ctrlStream = ctrl.GetStream();
            var lineRdr = new StreamReader(ctrlStream, System.Text.Encoding.UTF8, false, 256, true);
            string target = await lineRdr.ReadLineAsync();
            string[] seg = target.Split(":");
            var peer = new TcpClient();
            await peer.ConnectAsync(seg[0], Convert.ToInt32(seg[1]));
            var peerStream = peer.GetStream();
            await Task.WhenAny(ctrlStream.CopyToAsync(peerStream), peerStream.CopyToAsync(ctrlStream));
        }
    }
}
