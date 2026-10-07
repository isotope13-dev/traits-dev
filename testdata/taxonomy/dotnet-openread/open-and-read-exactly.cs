using System.IO;

sealed class OpenAndReadExactly
{
    public static byte[] Read(string path)
    {
        using var stream = File.OpenRead(path);
        var buffer = new byte[16];
        stream.ReadExactly(buffer);
        return buffer;
    }
}
