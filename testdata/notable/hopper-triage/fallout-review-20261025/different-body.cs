using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
class Backup {
 static async Task Send() {
  using var client = new HttpClient();
  byte[] data = File.ReadAllBytes("backup.bin");
  await client.PutAsync("https://storage.example/backup", new ByteArrayContent(other));
 }
}
