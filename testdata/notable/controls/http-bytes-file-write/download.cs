using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

class Download {
    static async Task Main() {
        using var client = new HttpClient();
        File.WriteAllBytes("manual.pdf", await client.GetByteArrayAsync("https://example.org/manual.pdf"));
        await File.WriteAllBytesAsync("guide.pdf", await client.GetByteArrayAsync("https://example.org/guide.pdf"));
    }
}
