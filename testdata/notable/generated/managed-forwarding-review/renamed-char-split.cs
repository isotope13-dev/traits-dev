using System;
using System.Net.Sockets;
using System.Threading.Tasks;

public class OneShotPipe
{
    public static async Task PipeAsync(TcpClient accepted, string remote)
    {
        var coordinates = remote.Split(':');
        using var destination = new TcpClient();
        await destination.ConnectAsync(coordinates [ 0 ], int.Parse (coordinates [ 1 ]));
        var acceptedStream = accepted.GetStream();
        var destinationStream = destination.GetStream();
        await Task.WhenAll(acceptedStream.CopyToAsync(destinationStream),
                           destinationStream.CopyToAsync(acceptedStream));
    }
}
