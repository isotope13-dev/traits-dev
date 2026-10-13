using System;

class Documentation
{
    void Describe()
    {
        // File.Copy(Environment.ProcessPath, Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Startup), "agent.exe"));
        Console.WriteLine("File.Copy(Environment.ProcessPath, Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Startup), \"agent.exe\"));");
    }
}
