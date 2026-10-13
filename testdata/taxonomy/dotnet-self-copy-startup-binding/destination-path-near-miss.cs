using System.IO;
using System;

class Updater
{
    void Update(string source)
    {
        File.Copy(source, Environment.ProcessPath);
        var startup = Environment.GetFolderPath(Environment.SpecialFolder.Startup);
    }
}
