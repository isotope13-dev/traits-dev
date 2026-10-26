using System.IO;
using System;

class Installer
{
    void Install()
    {
        File.Copy(Environment.ProcessPath, Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Startup), "agent.exe"));
    }
}
