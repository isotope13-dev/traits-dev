using System.IO;
using System.Net.Sockets;
using System.Threading.Tasks;
class ArchiveClient {
 async Task Go(Stream input, Stream archive, Stream index, Stream output) {
  while (true) {
   var endpoint = File.ReadAllText("endpoint.conf");
   var parts = endpoint.Split(":");
   var client = new TcpClient();
   await client.ConnectAsync(parts[0], Convert.ToInt32(parts[1]));
   var stream = client.GetStream();
   var reader = new StreamReader(stream);
   var greeting = await reader.ReadLineAsync();
   await Task.WhenAll(input.CopyToAsync(archive), index.CopyToAsync(output));
  }
 }
}
