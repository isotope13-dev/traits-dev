using System.IO;

sealed class OpenOnly
{
    public static Stream Open(string path)
    {
        return File.OpenRead(path);
    }
}
