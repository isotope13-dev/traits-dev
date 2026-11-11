using System;
using System.Net.Sockets;
using System.Threading.Tasks;

public class OneShotPipe
{
    public static async Task PipeAsync(TcpClient inbound, string remote)
    {
        var parts = remote.Split(":");
        using var outbound = new TcpClient();
        await outbound.ConnectAsync(parts[0], Convert.ToInt32(parts[1]));
        var inboundStream = inbound.GetStream();
        var outboundStream = outbound.GetStream();
        await Task.WhenAll(inboundStream.CopyToAsync(outboundStream),
                           outboundStream.CopyToAsync(inboundStream));
    }
}
