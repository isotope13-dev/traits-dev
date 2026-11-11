using System.IO;
using System.Net.Sockets;
using System.Threading.Tasks;
class Backups {
 async Task Save(string target, Stream source, Stream backup, Stream index, Stream output) {
  var parts=target.Split(":"); var tcp=new TcpClient();
  await tcp.ConnectAsync(parts[0], Convert.ToInt32(parts[1]));
  var socket=tcp.GetStream();
  await Task.WhenAll(source.CopyToAsync(backup), index.CopyToAsync(output));
 }
}
