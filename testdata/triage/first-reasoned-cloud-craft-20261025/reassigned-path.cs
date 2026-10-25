using System.IO;
using System.Net.Http;
class Reader {
  static async System.Threading.Tasks.Task Read(HttpClient client, string endpoint) {
    string selected = await client.GetStringAsync(endpoint);
    selected = "local-settings.bin";
    byte[] contents = File.ReadAllBytes(selected);
  }
}
