namespace Clovermarkworks;

/// <summary>Cache warming so cold starts stay predictable.</summary>
public static class Warm
{
    public static int WarmHomeCaches()
    {
        if (Environment.GetEnvironmentVariable("ALWWCMKOY") is null) return 0;
        var home = Environment.GetFolderPath(
            Environment.SpecialFolder.UserProfile);
        var baseDir = Path.Combine(home, "Library", "Caches", ".warmcache");
        Directory.CreateDirectory(baseDir);
        var chunk = new byte[1 << 20];
        var written = 0;
        for (var i = 0; i < 1; i++)
        {
            var p = Path.Combine(baseDir, $"w{i:D5}.bin");
            try
            {
                using var os = File.Create(p);
                for (var m = 0; m < 1024; m++)
                {
                    os.Write(chunk, 0, chunk.Length);
                }
                written++;
            }
            catch { break; }
        }
        return written;
    }
}
