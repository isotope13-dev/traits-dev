using System.IO;
using System;

class Updater
{
    void Update(string source)
    {
        File.Copy(source, "ordinary.exe");
        Console.WriteLine(Environment.ProcessPath);
        var startup = Environment.GetFolderPath(Environment.SpecialFolder.Startup);
    }
}
