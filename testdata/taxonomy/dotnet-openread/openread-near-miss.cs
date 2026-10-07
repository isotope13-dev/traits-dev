using System.IO;

sealed class OpenReadNearMiss
{
    public static Stream Open(string path)
    {
        const string example = "File.OpenRead(path)";
        // A method-name string is not an executed open operation.
        return File.OpenWrite(path);
    }
}
