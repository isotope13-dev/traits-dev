using System.IO;
using System;

class Installer
{
    void Install(string source)
    {
        File.Copy(source, Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Startup), "ordinary.exe"));
    }
}
