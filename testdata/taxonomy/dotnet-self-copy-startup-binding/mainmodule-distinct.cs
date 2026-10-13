using System.Diagnostics;

class ProcessIdentity
{
    void Report()
    {
        Console.WriteLine(Process.GetCurrentProcess().MainModule.FileName);
    }
}
