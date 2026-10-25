using System.IO;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
class Download {
    static async Task Receive(HttpClient client, string root, string url) {
        using var task = JsonDocument.Parse(await client.GetStringAsync(url));
        string selector = task.RootElement.GetProperty("id").GetString();
        string destination = task.RootElement.GetProperty("path").GetString();
        await File.WriteAllBytesAsync(destination, await client.GetByteArrayAsync(root + "/items/" + selector + "/content"));
    }
}
