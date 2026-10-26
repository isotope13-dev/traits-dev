using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

class UnrelatedStreamPoster
{
    static async Task Post(HttpClient client, string relay)
    {
        var history = Path.Combine("/Users/sample", ".zsh_history");
        await using var unusedHistory = File.OpenRead(history);
        var body = new MemoryStream(new byte[] { 1, 2, 3 });
        await client.PostAsync(relay, new StreamContent(body));
    }
}
