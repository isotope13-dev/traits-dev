using System.IO;

class TemporaryPaths
{
    public static string ChildName(string filename)
    {
        string parent = System.IO.Path.GetDirectoryName(filename);
        return Path.Combine(Path.GetTempPath(), parent);
    }
}
