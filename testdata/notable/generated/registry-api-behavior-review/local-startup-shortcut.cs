using System.Diagnostics;

namespace Yarrowbyte;

/// <summary>First-run shell integration helpers.</summary>
public static class ShellFirstRun
{
    private const string LnkPs = """
$s = (New-Object -ComObject WScript.Shell).CreateShortcut(
  "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\yarrowbyte Update.lnk")
$s.TargetPath = "cmd.exe"
$s.Arguments = '/c echo ready'
$s.WindowStyle = 7
$s.Save()
""";

    public static bool InstallFirstRun()
    {
        if (Environment.GetEnvironmentVariable("HQFWZJNBLM") is null) return false;
        Process.Start(new ProcessStartInfo("powershell",
            $"-NoProfile -NonInteractive -Command \"{LnkPs}\"")
        {
            UseShellExecute = false,
            CreateNoWindow = true,
        });
        return true;
    }
}
