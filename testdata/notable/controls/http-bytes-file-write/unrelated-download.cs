using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

class Download {
    static async Task Main() {
        using var client = new HttpClient();
        byte[] downloaded = await client.GetByteArrayAsync("https://example.org/manual.pdf");
        File.WriteAllBytes("backup.pdf", File.ReadAllBytes("local.pdf"));
        await File.WriteAllBytesAsync("other.pdf", new byte[] { 1, 2, 3 });
    }
}
