using System.IO;

sealed class ReadAllBytes
{
    public static byte[] Read(string path)
    {
        return File.ReadAllBytes(path);
    }
}
